"""
Joel Karie Allen
GIS-4080 Grzinic
27 AUG 2020
Term Project
"""

import arcpy
import string

arcpy.env.overwriteOutput = True

print("Starting Mapping...yes, I know runned is not a word")

### 1. Set up input paths, output paths, and project variables
workspace = "C:\\temp\\ALLEN_TermProject"
output = workspace + "\\Maps"
tempPDF = output + "\\temp.pdf"
finalPDF = output + "\\ALLENTermProjectMaps.pdf"
Shapefiles = workspace + "\\ShapeFiles"
GeoDatabase = "C:\\temp\\ALLEN_TermProject\\TermProject\\TermProject\\TermProject.gdb"
runFiles = workspace + "\\StravaFiles"
RunTracks = GeoDatabase + "\\RunTracks"
outProject = workspace + "\\TermProject"

# project variables
schemaType = "NO_TEST"
fieldMappings = ""
subtype = ""

### 2. Create Shapefile to hold all runs and add all runs from GPX files
# set workspace to directory of interest
arcpy.env.workspace = runFiles

# create list of all files ending in .shp
list_gpxfiles = arcpy.ListFiles("*.gpx")

# create blank Shapefile
arcpy.CreateFeatureclass_management(GeoDatabase, "RunTracks", "POLYLINE")

# this loop will accomplish steps 3-5
for file in list_gpxfiles:
    print(file + " started")

    ### 3. Convert the GPX file into in_memory features
    arcpy.GPXtoFeatures_conversion(file, 'in_memory\\runs')

    # Select only the track points
    arcpy.SelectLayerByAttribute_management('in_memory\\runs', 'NEW_SELECTION', "\"Type\" = 'TRKPT'")

    ### 4. Convert the tracks into lines. The 'Name' field creates unique tracks.
    arcpy.PointsToLine_management('in_memory\\runs', GeoDatabase + "\\tempRun", 'Name', '#', 'NO_CLOSE')

    print(file + " converted")

    ### 5. Add line to shapefile of all runs
    arcpy.Append_management(GeoDatabase + "\\tempRun", GeoDatabase + "\\RunTracks", schemaType, fieldMappings, subtype)
    print(file + ' added to Runtracks')

# switch the workspace to the Geodatabase
arcpy.env.workspace = GeoDatabase

### 6. Create layer of US counties which insect with runs
selectedCounties = arcpy.SelectLayerByLocation_management(Shapefiles + "\\Counties\\cb_2018_us_county_500k.shp",
                                                          "INTERSECT", RunTracks)
# Write the selected features to a new featureclass
arcpy.CopyFeatures_management(selectedCounties, "RunnedUsStates")
print("RunnedUsStates layer created\r")

### 7. Create layer of Canadian Provinces which insect with runs
selectedProvinces = arcpy.SelectLayerByLocation_management(Shapefiles + "\\Canada2\\Canada.shp", "INTERSECT", RunTracks)

# Write the selected features to a new featureclass
arcpy.CopyFeatures_management(selectedProvinces, "RunnedCanadaProvinces")
print("RunnedCanadaProvinces layer created\r")

### 8. Create layer of South African Provinces which insect with runs
selectedSAProvinces = arcpy.SelectLayerByLocation_management(
    Shapefiles + "\\South Africa\\District_Municipalities_2016.shp", "INTERSECT", RunTracks)

# Write the selected features to a new featureclass
arcpy.CopyFeatures_management(selectedSAProvinces, "RunnedSaProvinces")
print("RunnedSaProvinces layer created\r")

# variables for the new features
RunnedUsCountiesFeature = "C:\\temp\\ALLEN_TermProject\\TermProject\\TermProject\\TermProject.gdb\\RunnedUsStates"
RunnedCanadaProvincesFeature = "C:\\temp\\ALLEN_TermProject\\TermProject\\TermProject\\TermProject.gdb\\RunnedCanadaProvinces"
RunnedSAProvincesFeature = "C:\\temp\\ALLEN_TermProject\\TermProject\\TermProject\\TermProject.gdb\\RunnedSaProvinces"
RunTracksFeature = "C:\\temp\\ALLEN_TermProject\\TermProject\\TermProject\\TermProject.gdb\\RunTracks"
MetroAreasFeature = "C:\\temp\\ALLEN_TermProject\\TermProject\\TermProject\\TermProject.gdb\\MetroAreas"

#connect to the aprx and check status of maps and layers
aprx = arcpy.mp.ArcGISProject(r"C:\temp\ALLEN_TermProject\TermProject\TermProject\TermProject.aprx")
for m in aprx.listMaps():
    print("Status of aprx before addition of layers")
    print("Map: " + m.name)
    for lyr in m.listLayers():
        print("  " + lyr.name)
print("Layouts:")
for lyt in aprx.listLayouts():
    print(f"  {lyt.name} ({lyt.pageHeight} x {lyt.pageWidth} {lyt.pageUnits})")

### 9.  Add layers to first map
aprxMap = aprx.listMaps()[0]
aprxMap.addDataFromPath(RunnedUsCountiesFeature)
aprxMap.addDataFromPath(RunnedCanadaProvincesFeature)
aprxMap.addDataFromPath(RunnedSAProvincesFeature)
aprxMap.addDataFromPath(RunTracksFeature)

# check status of maps and layers after addition
for m in aprx.listMaps():
    print("Status of aprx after addition of layers")
    print("Map: " + m.name)
    for lyr in m.listLayers():
        print("  " + lyr.name)
print("Layouts:")
for lyt in aprx.listLayouts():
    print(f"  {lyt.name} ({lyt.pageHeight} x {lyt.pageWidth} {lyt.pageUnits})")

# save project (or all will be lost)
aprx.save()

### 10. add layers for World Map
aprxMap = aprx.listMaps()[1]
aprxMap.addDataFromPath(RunnedUsCountiesFeature)
aprxMap.addDataFromPath(RunnedCanadaProvincesFeature)
aprxMap.addDataFromPath(RunnedSAProvincesFeature)
aprxMap.addDataFromPath(RunTracksFeature)

# check new status of maps and layers
for m in aprx.listMaps():
    print("Status of aprx after addition of layers")
    print("Map: " + m.name)
    for lyr in m.listLayers():
        print("  " + lyr.name)
print("Layouts:")
for lyt in aprx.listLayouts():
    print(f"  {lyt.name} ({lyt.pageHeight} x {lyt.pageWidth} {lyt.pageUnits})")

# save the progress
aprx.save()

# paths for layouts
UsCountyLayer = workspace + "\\Counties.shp"
output = r"C:\temp\ALLEN_TermProject\Maps"
tempPDF = output + "\\temp.pdf"
finalPDF = output + "\\ALLENTermProject.pdf"

# Obtain pointers to project, map, later, layout, and map frame
mapx = aprx.listMaps()[0]
lyr = mapx.listLayers("RunnedUsStates")[0]
lyt = aprx.listLayouts("USRuns")[0]
mf = lyt.listElements('MAPFRAME_ELEMENT', "Map Frame")[0]
mapWorld = aprx.listMaps()[1]
lyr2 = mapWorld.listLayers("RunnedUsStates")[0]
mf2 = lyt.listElements('MAPFRAME_ELEMENT', "World Map Frame")[0]
symbLayer = mapx.listLayers("LineSymbology")
runTrackLayer = mapx.listLayers("RunTracks")


### 11. Create PDF and add maps by county and province
# Create empty PDF
pdfDoc = arcpy.mp.PDFDocumentCreate(finalPDF)

# loop through Counties shapefile:
with arcpy.da.SearchCursor(RunnedUsCountiesFeature, "NAME") as cursor:
    for row in cursor:
        # get the country name and add it to the whereClause and zoom in
        print(row[0] + " County")
        countyName = row[0]
        whereClause = """ "NAME" = '{0}' """.format(countyName)
        lyr.definitionQuery = whereClause
        mf.camera.setExtent(mf.getLayerExtent(lyr))
        mf.camera.scale *= 1.2
        lyr2.definitionQuery = whereClause
        mf2.camera.setExtent(mf2.getLayerExtent(lyr2))
        mf2.camera.scale *= 10

        # Obtain title element and change the text
        title = lyt.listElements('TEXT_ELEMENT', "Text")[0]
        # reformat county name
        newCountyName = str(countyName)
        newestName = newCountyName.lower()
        newestName = string.capwords(newestName)
        print(newestName + " County has been added to the PDF queue")

        # add name to title
        title.text = newestName + " County, USA"

        # Export new map to PDF
        lyt.exportToPDF(tempPDF)
        pdfDoc.appendPages(tempPDF)

# loop through SAProvince shapefile with SA provinces
lyr = mapx.listLayers("RunnedSaProvinces")[0]
lyt = aprx.listLayouts("SARUns")[0]
mf = lyt.listElements('MAPFRAME_ELEMENT', "Map Frame")[0]
mapWorld = aprx.listMaps()[1]
lyr2 = mapWorld.listLayers("RunnedSaProvinces")[0]
mf2 = lyt.listElements('MAPFRAME_ELEMENT', "World Map Frame")[0]

with arcpy.da.SearchCursor(RunnedSAProvincesFeature, "PROVINCE") as cursor:
    for row in cursor:
        # get the province name and add it to the whereClause and zoom in
        print(row[0] + " Province")
        countyName = row[0]
        whereClause = """ "PROVINCE" = '{0}' """.format(countyName)
        lyr.definitionQuery = whereClause
        mf.camera.setExtent(mf.getLayerExtent(lyr))
        mf.camera.scale *= 1.2
        lyr2.definitionQuery = whereClause
        mf2.camera.setExtent(mf2.getLayerExtent(lyr2))
        mf2.camera.scale *= 10

        # Obtain title element and change the text
        title = lyt.listElements('TEXT_ELEMENT', "Text")[0]

        # reformat province name
        newCountyName = str(countyName)
        newestName = newCountyName.lower()
        newestName = string.capwords(newestName)
        print(newestName + " Province has been added to the PDF queue")

        # add name to title
        title.text = newestName + " Province, South Africa"

        # Export new map to PDF
        lyt.exportToPDF(tempPDF)
        pdfDoc.appendPages(tempPDF)

# Export new map to PDF
lyt.exportToPDF(tempPDF)
pdfDoc.appendPages(tempPDF)

print("PDF exported to Maps folder")
# Clean up
pdfDoc.saveAndClose()
del pdfDoc
del aprx
