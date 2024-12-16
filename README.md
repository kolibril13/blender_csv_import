# blender_csv_import

https://extensions.blender.org/add-ons/csv-importer/



A simple and fast CSV file importer.

<img width="500" alt="thumb_almost_color" src="https://github.com/user-attachments/assets/0306c8ca-590e-4c14-9d3d-d5b579ff250b" />



## How to Use

Option 1: Drag and drop your CSV file directly into Blender’s viewport.

Option 2: Use the menu:
File → Import → CSV

### **Using the Data**  
- The imported data will appear in Blender’s **Spreadsheet Editor**.  
- Use the **Named Attribute** in **Geometry Nodes** to access the imported data.


And the data will show up in the speadsheet:

<img width="900" alt="image" src="https://github.com/user-attachments/assets/36f7e277-ab73-4335-936c-9ca25a32683b" />



you can reproduce the above example with this geometry nodes setup.
The corresponding Blender file can be downloaded [here](https://github.com/kolibril13/blender_csv_import/blob/main/generate_data/example_file_california_bounding_box.blend)

<img width="1471" alt="image" src="https://github.com/user-attachments/assets/515e7727-e995-4672-918a-1234c9fd0ad7" />








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

