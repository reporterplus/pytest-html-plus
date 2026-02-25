def resolve_driver(item):
   candidates = getattr(item, "funcargs", {})

   # 1. Priority: 'page'
   page = candidates.get("page")
   if page and hasattr(page, "screenshot"):
       return page

   # 2. .screenshot() fallback
   for val in candidates.values():
       if hasattr(val, "screenshot"):
           return val

   # 3. Selenium fallback
   for val in candidates.values():
       if hasattr(val, "get_screenshot_as_file"):
           return val

   # 4. Manual override
   if hasattr(item, "page_for_screenshot"):
       print("[resolve_driver] Using manually attached screenshot object")
       return item.page_for_screenshot

   return None


import os


def sanitize_filename(name):
   return "".join(c if c.isalnum() else "_" for c in name)

def take_screenshot_generic(path, item, driver):
   os.makedirs(path, exist_ok=True)
   filename = os.path.join(path, f"{sanitize_filename(item.name)}_failure.png")

   if hasattr(driver, "screenshot"):
       driver.screenshot(path=filename)
   elif hasattr(driver, "save_screenshot"):
       driver.save_screenshot(filename)
   elif hasattr(driver, "get_screenshot_as_file"):
       driver.get_screenshot_as_file(filename)
   else:
       raise RuntimeError(f"No screenshot method found for: {type(driver)}")

   return filename
