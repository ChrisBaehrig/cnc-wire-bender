#Christopher Behrends 
#Koordinaten auslesen Biegemaschine in CSV

import adsk.core, adsk.fusion, traceback

pipeRadius = 0.15
pipeThickness = '3mm'
    
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
            return
        
        sel = ui.selectEntity('Select a path to create a pipe', 'Edges,SketchCurves')
        selObj = sel.entity
        
        comp = design.rootComponent
        
        # create path
        feats = comp.features
        chainedOption = adsk.fusion.ChainedCurveOptions.connectedChainedCurves
        if adsk.fusion.BRepEdge.cast(selObj):
            chainedOption = adsk.fusion.ChainedCurveOptions.tangentChainedCurves
        path = adsk.fusion.Path.create(selObj, chainedOption)
        path = feats.createPath(selObj)
        
        # create profile
        planes = comp.constructionPlanes
        planeInput = planes.createInput()
        planeInput.setByDistanceOnPath(selObj, adsk.core.ValueInput.createByReal(0))
        plane = planes.add(planeInput)
        
        sketches = comp.sketches
        sketch = sketches.add(plane)
        
        center = plane.geometry.origin
        center = sketch.modelToSketchSpace(center)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(center, pipeRadius)
        profile = sketch.profiles[0]
        
        # create sweep
        sweepFeats = feats.sweepFeatures
        sweepInput = sweepFeats.createInput(profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        sweepInput.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
        sweepFeat = sweepFeats.add(sweepInput)
        

        # Add construction plane by distance on path
        # Prompt the user for a string and validate it's valid.
        isValid = False
        input = '10'  # The initial default value.
        while not isValid:
            # Get a string from the user.
            retVals = ui.inputBox('Enter number of Steps', 'Steps', input)
            if retVals[0]:
                (input, isCancelled) = retVals
            
            # Exit the program if the dialog was cancelled.
            if isCancelled:
                return
            
            # Check that a valid length description was entered.
            unitsMgr = design.unitsManager
            try:
                realValue = unitsMgr.evaluateExpression(input, unitsMgr.defaultLengthUnits)
                isValid = True
            except:
                # Invalid expression so display an error and set the flag to allow them
                # to enter a value again.
                ui.messageBox('"' + input + '" is not a valid length expression.', 'Invalid entry', 
                              adsk.core.MessageBoxButtonTypes.OKButtonType, 
                              adsk.core.MessageBoxIconTypes.CriticalIconType)
                isValid = False
        
        Steps = int(input)
        ui.messageBox('Anzahl der Schritte: ' + str(Steps) )
  
        #Steps= 5       #Anzahl der Ebenen
        DistanceSteps= 1/Steps
        msg = 'Zeile; X-Koordinate; Y-Koordinate; Z-Koordinate; X-Vektor; Y-Vektor; Z-Vektor\n'


        #Erstellen der Koordinaten        
        for i in range(Steps+1):
            planeInput.setByDistanceOnPath(path, adsk.core.ValueInput.createByReal(i*DistanceSteps))
            plane2 = planes.add(planeInput)
            Coordinate = plane2.geometry.origin
            Vector = plane2.geometry.normal
            text = str(i) + '; ' + str(Coordinate.asArray()) + '; '+ str(Vector.asArray()) + '\n'
            text = text.replace('(', '')
            text = text.replace(')', '')
            text = text.replace(',', ';')
            msg += text.replace('.', ',')

        #Schreiben der Koordinaten
        dialogResult = ui.messageBox('Koordinaten jetzt speichern?', 'UI Report Type', adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType, adsk.core.MessageBoxIconTypes.QuestionIconType) 
        if dialogResult == adsk.core.DialogResults.DialogYes:

            fileDialog = ui.createFileDialog()
            fileDialog.isMultiSelectEnabled = False
            fileDialog.title = "Specify result filename"
            fileDialog.filter = 'Text files (*.csv)'
            fileDialog.filterIndex = 0
            dialogResult = fileDialog.showSave()
            if dialogResult == adsk.core.DialogResults.DialogOK:
                filename = fileDialog.filename
            else:
                return

            output = open(filename, 'w')
            output.writelines(msg)
            output.close()
            
            ui.messageBox('File written to "' + filename + '"')           

        else:
            return   
        
        app.activeViewport.refresh()
        ui.messageBox('Done')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
