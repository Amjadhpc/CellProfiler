"""Modules - pipeline processing modules for CellProfiler

CellProfiler is distributed under the GNU General Public License.
See the accompanying file LICENSE for details.

Developed by the Broad Institute
Copyright 2003-2010

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
"""
__version__="$Revision$"

import re
import sys
import os.path
import glob
import cellprofiler.cpmodule as cpm
from cellprofiler.modules.plugins import plugin_list

# python modules and their corresponding cellprofiler.module classes
pymodule_to_cpmodule = {'align' : 'Align',
                        'applythreshold' : 'ApplyThreshold',
                        'calculateimageoverlap' : 'CalculateImageOverlap',
                        'calculatemath' : 'CalculateMath',
                        'calculatestatistics' : 'CalculateStatistics',
                        'classifyobjects' : 'ClassifyObjects',
                        'colortogray' : 'ColorToGray',
                        'conservememory' : 'ConserveMemory',
                        'convertobjectstoimage' : 'ConvertObjectsToImage',
                        'correctilluminationcalculate' : 'CorrectIlluminationCalculate',
                        'correctilluminationapply' : 'CorrectIlluminationApply',
                        'createbatchfiles' : 'CreateBatchFiles',
                        'crop' : 'Crop',
                        'definegrid' : 'DefineGrid',
                        'displaydensityplot' : 'DisplayDensityPlot',
                        'displaydataonimage' : 'DisplayDataOnImage',
                        'displayhistogram' : 'DisplayHistogram',
                        'displayscatterplot' : 'DisplayScatterPlot',
                        'editobjectsmanually' : 'EditObjectsManually',
                        'enhanceedges' : 'EnhanceEdges',
                        'enhanceorsuppressfeatures' : 'EnhanceOrSuppressFeatures',
                        'expandorshrinkobjects' : 'ExpandOrShrinkObjects',
                        'exporttodatabase' : 'ExportToDatabase',
                        'exporttospreadsheet' : 'ExportToSpreadsheet',
                        'filterobjects' : 'FilterObjects',
                        'flagimage' : 'FlagImage',
                        'flipandrotate' : 'FlipAndRotate',
                        'graytocolor' : 'GrayToColor',
                        'identifyobjectsingrid': 'IdentifyObjectsInGrid',
                        'identifyobjectsmanually': 'IdentifyObjectsManually',
                        'identifyprimaryobjects' : 'IdentifyPrimaryObjects',
                        'identifysecondaryobjects' : 'IdentifySecondaryObjects',
                        'identifytertiaryobjects' : 'IdentifyTertiaryObjects',
                        'imagemath' : 'ImageMath',
                        'invertforprinting' : 'InvertForPrinting',
                        'loadimages' : 'LoadImages',
                        #'loadimagesnew' : 'LoadImagesNew',
                        'loadsingleimage' : 'LoadSingleImage',
                        'loaddata' : 'LoadData',
                        'makeprojection' : 'MakeProjection',
                        'maskimage' : 'MaskImage',
                        'maskobjects' : 'MaskObjects',
                        'measurecorrelation' : 'MeasureCorrelation',
                        'measureimageareaoccupied' : 'MeasureImageAreaOccupied',
                        'measureimagegranularity' : 'MeasureImageGranularity',
                        'measureimageintensity' : 'MeasureImageIntensity',
                        'measureimagequality' : 'MeasureImageQuality',
                        'measureobjectintensity' : 'MeasureObjectIntensity',
                        'measureobjectsizeshape' : 'MeasureObjectSizeShape',
                        'measureobjectneighbors' : 'MeasureObjectNeighbors',
                        'measureobjectradialdistribution' : 'MeasureObjectRadialDistribution',
                        'measureneurons': 'MeasureNeurons',
                        'measuretexture' : 'MeasureTexture',
                        'morph' : 'Morph',
                        'overlayoutlines' : 'OverlayOutlines',
                        'pausecellprofiler': 'PauseCellProfiler',
                        'relateobjects' : 'RelateObjects',
                        'reassignobjectnumbers': 'ReassignObjectNumbers',
                        'renameorrenumberfiles': 'RenameOrRenumberFiles',
                        'rescaleintensity' : 'RescaleIntensity',
                        'resize' : 'Resize',
                        'saveimages' : 'SaveImages',
                        'sendemail' : 'SendEmail',
                        'smooth' : 'Smooth',
                        'trackobjects' : 'TrackObjects',
                        'tile' : 'Tile',
                        'calculateimageoverlap' : 'CalculateImageOverlap'
                        }

# the builtin CP modules that will be loaded from the cellprofiler.modules directory
builtin_modules = ['align',
                   'applythreshold',
                   'calculateimageoverlap',
                   'calculatemath',
                   'calculatestatistics',
                   'classifyobjects',
                   'colortogray',
                   'conservememory',
                   'convertobjectstoimage',
                   'correctilluminationcalculate',
                   'correctilluminationapply',
                   'createbatchfiles',
                   'crop',
                   'definegrid',
                   'displaydataonimage',
                   'displaydensityplot',
                   'displayhistogram',
                   'displayscatterplot',
                   'editobjectsmanually',
                   'enhanceedges',
                   'enhanceorsuppressfeatures',
                   'expandorshrinkobjects',
                   'exporttodatabase',
                   'exporttospreadsheet',
                   'filterobjects',
                   'flagimage',
                   'flipandrotate',
                   'graytocolor',
                   'identifyobjectsingrid',
                   'identifyobjectsmanually',
                   'identifyprimaryobjects',
                   'identifysecondaryobjects',
                   'identifytertiaryobjects',
                   'imagemath',
                   'invertforprinting',
                   'loadimages',
                   #'loadimagesnew',
                   'loadsingleimage',
                   'loaddata',
                   'makeprojection',
                   'maskimage',
                   'maskobjects',
                   'measurecorrelation',
                   'measureimageareaoccupied',
                   'measureimagegranularity',
                   'measureimageintensity',
                   'measureimagequality',
                   'measureobjectintensity',
                   'measureobjectsizeshape',
                   'measureobjectneighbors',
                   'measureobjectradialdistribution',
                   'measureneurons',
                   'measuretexture',
                   'morph',
                   'overlayoutlines',
                   'pausecellprofiler',
                   'relateobjects',
                   'reassignobjectnumbers',
                   'renameorrenumberfiles',
                   'rescaleintensity',
                   'resize',
                   'saveimages',
                   'sendemail',
                   'smooth',
                   'trackobjects',
                   'tile',
                   ]

# CP-Matlab to CP-python module substitutions
substitutions = {'Average': 'MakeProjection',
                 'CalculateRatios': 'CalculateMath',
                 'ClassifyObjectsByTwoMeasurements' : 'ClassifyObjects',
                 'Combine': 'ImageMath',
                 'cellprofiler.modules.converttoimage.ConvertToImage': 'ConvertObjectsToImage',
                 'ConvertToImage': 'ConvertObjectsToImage',
                 'cellprofiler.modules.enhanceorsuppressspeckles.EnhanceOrSuppressSpeckles': 'EnhanceOrSuppressFeatures',
                 'EnhanceOrSuppressSpeckles': 'EnhanceOrSuppressFeatures',
                 'Exclude': 'MaskObjects',
                 'cellprofiler.modules.expandorshrink.ExpandOrShrink': 'ExpandOrShrinkObjects',
                 'ExpandOrShrink':'ExpandOrShrinkObjects',
                 'ExportToExcel': 'ExportToSpreadsheet',
                 'cellprofiler.modules.exporttoexcel.ExportToExcel': 'ExportToSpreadsheet',
                 'FilterByObjectMeasurement': 'FilterObjects',
                 'cellprofiler.modules.filterbyobjectmeasurement.FilterByObjectMeasurement': 'FilterObjects',
                 'FindEdges':'EnhanceEdges',
                 'cellprofiler.modules.findedges.FindEdges':'EnhanceEdges',
                 'FlagImageForQC' : 'FlagImage',
                 'Flip' : 'FlipAndRotate',
                 'IdentifyPrimManual': 'IdentifyObjectsManually',
                 'cellprofiler.modules.identifyprimautomatic.IdentifyPrimAutomatic': 'IdentifyPrimaryObjects',
                 'IdentifyPrimAutomatic':'IdentifyPrimaryObjects',
                 'cellprofiler.modules.identifysecondary.IdentifySecondary': 'IdentifySecondaryObjects',
                 'IdentifySecondary': 'IdentifySecondaryObjects',
                 'cellprofiler.modules.identifytertiarysubregion.IdentifyTertiarySubregion': 'IdentifyTertiaryObjects',
                 'IdentifyTertiarySubregion': 'IdentifyTertiaryObjects',
                 'cellprofiler.modules.imageconvexhull.ImageConvexHull': 'Morph',
                 'ImageConvexHull': 'Morph',
                 'InvertIntensity': 'ImageMath',
                 'KeepLargestObject' : 'FilterObjects',
                 'cellprofiler.modules.loadtext.LoadText': 'LoadData',
                 'LoadText': 'LoadData',
                 'cellprofiler.modules.measureobjectareashape.MeasureObjectAreaShape':'MeasureObjectSizeShape',
                 'MeasureObjectAreaShape':'MeasureObjectSizeShape',
                 'MeasureImageSaturationBlur': 'MeasureImageQuality',
                 'MeasureRadialDistribution' : 'MeasureObjectRadialDistribution',
                 'Multiply': 'ImageMath',
                 'PlaceAdjacent': 'Tile',
                 'cellprofiler.modules.relabelobjects.RelabelObjects':'ReassignObjectNumbers',
                 'RelabelObjects': 'ReassignObjectNumbers',
                 'cellprofiler.modules.relate.Relate': 'RelateObjects',
                 'Relate': 'RelateObjects',
                 'Rotate' : 'FlipAndRotate',
                 'SmoothOrEnhance' : 'Smooth',
                 'SmoothKeepingEdges' : 'Smooth',
                 'cellprofiler.modules.speedupcellprofiler.SpeedUpCellProfiler':'ConserveMemory',
                 'SpeedUpCellProfiler':'ConserveMemory',
                 'SplitIntoContiguousObjects': 'ReassignObjectNumbers',
                 'Subtract': 'ImageMath',
                 'UnifyObjects': 'ReassignObjectNumbers',
                 'cellprofiler.modules.overlay_outlines.OverlayOutlines':'OverlayOutlines',
                 'CorrectIllumination_Apply': 'CorrectIlluminationApply',
                 'CorrectIllumination_Calculate': 'CorrectIlluminationCalculate'
                 }

all_modules = {}
svn_revisions = {}
pymodules = []
badmodules = []
datatools = []

do_not_override = ['__init__', 'set_settings', 'create_from_handles', 'test_valid', 'module_class']
should_override = ['create_settings', 'settings', 'run']

def check_module(module, name):
    if hasattr(module, 'do_not_check'):
        return
    assert name == module.module_name, "Module %s should have module_name %s (is %s)"%(name, name, module.module_name)
    for method_name in do_not_override:
        assert getattr(module, method_name) == getattr(cpm.CPModule, method_name), "Module %s should not override method %s"%(name, method_name)
    for method_name in should_override:
        assert getattr(module, method_name) != getattr(cpm.CPModule, method_name), "Module %s should override method %s"%(name, method_name)
    

def find_cpmodule_name(m):
    for v, val in m.__dict__.iteritems():
        if isinstance(val, type) and issubclass(val, cpm.CPModule):
            return val.module_name
    raise "Could not find cpm.CPModule class in %s"%(m.__file__)

def fill_modules():
    del pymodules[:]
    del badmodules[:]
    del datatools[:]
    all_modules.clear()
    svn_revisions.clear()

    def add_module(mod, check_svn):
        try:
            m = __import__(mod, globals(), locals(), ['__all__'], 0)
            name = find_cpmodule_name(m)
        except Exception, e:
            import traceback
            print traceback.print_exc(e)
            badmodules.append((mod, e))
            return

        try:
            pymodules.append(m)
            if name in all_modules:
                sys.stderr.write("Warning, multiple definitions of module %s\n\told in %s\n\tnew in %s\n"%(name, sys.modules[all_modules[name].__module__].__file__, m.__file__))
            all_modules[name] = m.__dict__[name]
            check_module(m.__dict__[name], name)
            # attempt to instantiate
            all_modules[name]()
            if hasattr(all_modules[name], "run_as_data_tool"):
                datatools.append(name)
            if check_svn and hasattr(m, '__version__'):
                match = re.match('^\$Revision: ([0-9]+) \$$', m.__version__)
                if match is not None:
                    svn_revisions[name] = match.groups()[0]
        except Exception, e:
            import traceback
            print traceback.print_exc(e)
            badmodules.append((mod, e))
            if name in all_modules:
                del all_modules[name]
                del pymodules[-1]

    for mod in builtin_modules:
        add_module('cellprofiler.modules.'+ mod, True)

    for mod in plugin_list():
        add_module('cellprofiler.modules.plugins.' + mod, False)

    datatools.sort()
    if len(badmodules) > 0:
        print "could not load these modules", badmodules

fill_modules()        
    
__all__ = ['instantiate_module', 'get_module_names', 'reload_modules', 
           'output_module_html']

replaced_modules = {
    'LoadImageDirectory':['LoadImages','LoadData'],
    'GroupMovieFrames':['LoadImages'],
    'IdentifyPrimLoG':['IdentifyPrimaryObjects'],
    'FileNameMetadata':['LoadImages']
    }
depricated_modules = [
    'CorrectIllumination_Calculate_kate',
    'SubtractBackground'
    ]
unimplemented_modules = [
    'LabelImages', 'Restart', 'SplitOrSpliceMovie'
    ]
def instantiate_module(module_name):
    if module_name in substitutions: 
        module_name = substitutions[module_name]
    module_class = module_name.split('.')[-1]
    if not all_modules.has_key(module_class):
        if module_class in unimplemented_modules:
            raise ValueError(("The %s module has not yet been implemented. "
                              "It will be available in a later version "
                              "of CellProfiler.") % module_class)
        if module_class in depricated_modules:
            raise ValueError(("The %s module has been depricated and will "
                              "not be implemented in CellProfiler 2.0.") %
                             module_class)
        if replaced_modules.has_key(module_class):
            raise ValueError(("The %s module no longer exists. You can find "
                              "similar functionality in: %s") %
                             (module_class, ", ".join(replaced_modules[module_class])))
        raise ValueError("Could not find the %s module"%module_class)
    module = all_modules[module_class]()
    if svn_revisions.has_key(module_name):
        module.svn_version = svn_revisions[module_name]
    return module

def get_module_names():
    return all_modules.keys()

def get_data_tool_names():
    return datatools

def reload_modules():
    for m in pymodules:
        try:
            reload(m)
        except:
            pass
    fill_modules()
    
def output_module_html():
    '''Output an HTML page for each module'''
    root = os.path.split(__file__)[0]
    if len(root) == 0:
        root = os.curdir
    root = os.path.split(os.path.abspath(root))[0] # Back up one level
    webpage_path = os.path.join(root, 'help')
    if not (os.path.exists(webpage_path) and os.path.isdir(webpage_path)):
        try:
            os.mkdir(webpage_path)
        except IOError:
            webpage_path = root
    index_fd = open(os.path.join(webpage_path,'module_index.html'),'w')
        
    index_fd.write("""
<html style="font-family:arial">
<head>
    <title>Modules</title>
</head>
<body>
<h1><a name = "modules">Modules</a></h1>
<ul>\n""")
    d = {}
    module_dir = 'modules'
    module_path = os.path.join(webpage_path,module_dir)
    if not (os.path.exists(module_path) and os.path.isdir(module_path)):
        try:
            os.mkdir(module_path)
        except IOError:
            raise ValueError("Could not create directory %s" % module_path)
        
    for module_name in get_module_names():
        module = instantiate_module(module_name)
        if not d.has_key(module.category):
            d[module.category] = {}
        d[module.category][module_name] = module
        fd = open(os.path.join(module_path,"%s.html" % module_name), "w")
        fd.write(module.get_help())
        fd.close()
    for category in sorted(d.keys()):
        sub_d = d[category]
        index_fd.write("<li><b>%s</b><br><ul>\n"%category)
        for module_name in sorted(sub_d.keys()):
            index_fd.write("<li><a href='%s.html'>%s</a></li>\n" %
                           (os.path.join(module_dir,module_name), module_name))
        index_fd.write("</ul></li>\n")
    index_fd.write("</ul></body>\n")
    index_fd.close()
        