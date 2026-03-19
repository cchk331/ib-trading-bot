#!/bin/bash
set -e

echo "=== IB Trading Bot - Oracle VM Setup ==="

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git xvfb unzip wget

# Create app directory
mkdir -p ~/ib-trading-bot
cd ~/ib-trading-bot

# Clone repo (you'll need to set up SSH key or token)
# git clone https://github.com/cchk331/ib-trading-bot.git .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install IB Gateway
echo "=== Installing IB Gateway ==="
mkdir -p ~/ib-gateway
cd ~/ib-gateway
wget -q https://download2.interactivebrokers.com/installers/ibgateway/stable-standalone/ibgateway-stable-standalone-linux-x64.sh
chmod +x ibgateway-stable-standalone-linux-x64.sh
sudo ./ibgateway-stable-standalone-linux-x64.sh -q

# Install IBC (IB Controller for headless operation)
echo "=== Installing IBC ==="
mkdir -p ~/ibc
cd ~/ibc
wget -q https://github.com/IbcAlpha/IBC/releases/download/3.18.0/IBCLinux-3.18.0.zip
unzip -o IBCLinux-3.18.0.zip
chmod +x *.sh

# Create IBC config
cat > ~/ibc/config.ini << 'EOF'
LogToConsole=no
FIXLogging=no
IbLoginId=
IbPassword=
TradingMode=paper
AcceptIncomingConnectionAction=accept
AcceptNonBrokerageAccountWarning=yes
AllowBlindTrading=yes
DismissPasswordExpiryWarning=yes
DismissNSEComplianceNotice=yes
ExistingSessionDetectedAction=primary
OverrideTwsApiPort=4002
EOF

# Create startup script for IB Gateway
cat > ~/start_ib_gateway.sh << 'EOF'
#!/bin/bash
export DISPLAY=:1
Xvfb :1 -screen 0 1024x768x24 &
sleep 2
~/ibc/scripts/ibcstart.sh -g
EOF
chmod +x ~/start_ib_gateway.sh

# Create logs directory
mkdir -p ~/ib-trading-bot/logs

# Copy systemd service
sudo cp ~/ib-trading-bot/scripts/trading_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable trading_bot.service

echo "=== Setup complete ==="
echo "Next steps:"
echo "1. Edit ~/ibc/config.ini with your IB credentials"
echo "2. Edit ~/ib-trading-bot/.env with your settings"
echo "3. sudo systemctl start trading_bot"
echo "4. Check logs: journalctl -u trading_bot -f"
