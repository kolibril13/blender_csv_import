import bpy
import csv_importer as cs
import databpy as db
import time
import pytest

def test_reload_csv(tmp_path):
    # create a temporary file
    test_file = tmp_path / "test.csv"
    with open(test_file, 'w') as f:
        f.write('x,y,z\n')
        f.write('0,0,0\n')
    
    # load initial file
    bob = db.BlenderObject(cs.load_csv(str(test_file)))
    
    # verify initial point exists
    assert len(bob) == 1
    
    # append more points
    with open(test_file, 'a') as f:
        f.write('1,1,1\n')
        f.write('2,2,2\n')
    
    # reload file
    bob.object.select_set(True)
    bpy.context.view_layer.objects.active = bob.object
    bpy.ops.csv.reload_data(filepath=str(test_file))
    
    # verify new points exist
    assert len(bob.position) == 3
