# blender_csv_import

https://extensions.blender.org/add-ons/csv-importer/



A simple and fast CSV file importer.

## How to Use

Option 1: Drag and drop your CSV file directly into Blender’s viewport.

Option 2: Use the menu:
File → Import → CSV

### **Using the Data**  
- The imported data will appear in Blender’s **Spreadsheet Editor**.  
- Use the **Named Attribute** in **Geometry Nodes** to access the imported data.


And the data will show up in the speadsheet:

![alt text](image-1.png)


# Using data with Geometry Nodes:



# Development instructions

1. Install https://github.com/JacquesLucke/blender_vscode
2. Enable the setting "Blender › Addon: Reload On Save"
3. Command+Shift+P -> Blender: Build and Start
4. Start coding with __init__.py

### Build the extension:

For downloading the wheels files, run: 
```
/Applications/Blender.app/Contents/MacOS/Blender -b -P build.py
```
For building the app for all platforms, run
```
/Applications/Blender.app/Contents/MacOS/Blender --command extension build --split-platforms
```

