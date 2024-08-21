Workstation Setup Steps

MacOS

1. Install OS Updates
2. Install Chrome, Set as default
2. Install VPN, Enable
3. Install Homebrew:
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
4. Install kitty terminal
	brew install kitty
5. Make bash default shell

Update Unity Game Client / Download Client

1. Build Game as MacOS app.
2. Run `hdiutil create -format UDZO -srcfolder game.app game.dmg` to generate disk image.
3. Run `scp game.dmg root@144.202.111.41:~/downloads/vX/game.dmg` to copy to babu.