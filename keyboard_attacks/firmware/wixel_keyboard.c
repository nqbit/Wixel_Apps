#include <wixel.h>
#include <usb.h>
#include <usb_hid.h>

// Paste attack here (i.e. replace the attack[] array)
static uint8 attack[] = { 0x01, 0xFF, 0xFF };

void main() {
  uint16 i = 0;
  uint16 default_delay = 0;
  uint32 size = sizeof(attack);
  systemInit();
  usbInit();

  // Wait 5 seconds (This is an arbitrary number that I find to work.)
  // TODO(nqbit): Add in option to escape with button press.
  for (i = 0; i < 50; i++) {
    boardService();
    usbHidService();
    delayMs(50);
    LED_YELLOW(1);
    delayMs(50);
    LED_YELLOW(0);
  }
    
  LED_RED(1);
  while(usbHidKeyboardInputUpdated) {
    boardService();
    usbHidService();
  }
    
  for (i = 0; i < size; i++) {
    switch(attack[i]) {
    case 0x00:
      i+=2;
      default_delay = (attack[i-1] << 8) | attack[i];
      break;
    case 0x01:
      i+=2;
      delayMs((attack[i-1] << 8) | attack[i]);
      break;
    case 0x02: 
      i+=1;
      usbHidKeyboardInput.modifiers = attack[i];
      break;
    case 0x03:
      i+=1;
      usbHidKeyboardInput.keyCodes[0] = attack[i];
      break;
    case 0x13:
      i+=1;
      usbHidKeyboardInput.keyCodes[1] = attack[i];
      break;
    case 0x23:
      i+=1;
      usbHidKeyboardInput.keyCodes[2] = attack[i];
      break;
    case 0x33:
      i+=1;
      usbHidKeyboardInput.keyCodes[3] = attack[i];
      break;
    case 0x43:
      i+=1;
      usbHidKeyboardInput.keyCodes[4] = attack[i];
      break;
    case 0x53:
      i+=1;
      usbHidKeyboardInput.keyCodes[5] = attack[i];
      break;
    case 0x04:
      i+=1;
      usbHidKeyboardInput.keyCodes[0] = attack[i];
      usbHidKeyboardInputUpdated = 1;
      while(usbHidKeyboardInputUpdated) {
        boardService();
        usbHidService(); 
      }
      boardService();
      usbHidService();
      // Send a key up event
      usbHidKeyboardInput.keyCodes[0] = 0;
      usbHidKeyboardInput.keyCodes[1] = 0;
      usbHidKeyboardInput.keyCodes[2] = 0;
      usbHidKeyboardInput.keyCodes[3] = 0;
      usbHidKeyboardInput.keyCodes[4] = 0;
      usbHidKeyboardInput.keyCodes[5] = 0;
      usbHidKeyboardInput.modifiers = 0;
      usbHidKeyboardInputUpdated = 1;
      while(usbHidKeyboardInputUpdated) {
        boardService();
        usbHidService(); 
      }
      boardService();
      usbHidService();
      break;
    default:
      break;
    }

    delayMs(default_delay);
  }
  boardService();
  usbHidService(); 
  while(usbHidKeyboardInputUpdated) {
    boardService();
    usbHidService(); 
  }

  // Indicate task complete
  delayMs(500);
  LED_RED(0);
  delayMs(500);
  LED_RED(1);
  LED_YELLOW(1);
}
