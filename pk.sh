#!/bin/bash

APP_NAME="MyTool"
APP_PATH="dist/${APP_NAME}.app"
DMG_NAME="${APP_NAME}.dmg"
STAGE="dmg-root"

rm -rf "$STAGE" "$DMG_NAME"

# 确保签名
xattr -cr "$APP_PATH"
codesign --deep --force --sign - "$APP_PATH"

# 准备 dmg 结构
mkdir -p "$STAGE"
cp -R "$APP_PATH" "$STAGE/"
ln -s /Applications "$STAGE/Applications"

# 打包
hdiutil create "$DMG_NAME" \
  -volname "${APP_NAME} Installer" \
  -srcfolder "$STAGE" \
  -fs HFS+ \
  -format UDZO

echo "✅ 已打包为 $DMG_NAME"