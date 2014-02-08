#!/usr/bin/python
"""
***************************************************************************
qgis20_api_check.py
---------------------
Date : July 2013
Copyright : (C) 2013 by Luigi Pirelli
Email : luipir at gmail.com
***************************************************************************
* *
* This program is free software; you can redistribute it and/or modify *
* it under the terms of the GNU General Public License as published by *
* the Free Software Foundation; either version 2 of the License, or *
* (at your option) any later version. *
* *
***************************************************************************
"""
import sys, os, getopt, re

def usage():
    print "usage: ", sys.argv[0], "<path to parse of file>"

def walkerror(err):
    print "WALK ERROR: "+str(err)

def grep(filetogrep, pattern):
    with open(filetogrep, "r") as fin:
        matches = ( (lineindex, re.match(pattern, line), line) for lineindex, line in enumerate(fin) )
        return [match for match in matches if match[0] != -1]

def check(checkList, fileToCheck):
    for pattern, message in checkList:
        matches = grep(fileToCheck, ".*%s.*"%re.escape(pattern) )
        if matches:
            for lineindex, match, line in matches:
                if match:
                    print "LINE %d found \"%s\" IN: %s" % (lineindex+1, pattern, line[:-1])
                    print "\tTODO: %s \n" % message
    
# thinks to check from this HOWTO
# http://hub.qgis.org/wiki/quantum-gis/API_changes_for_version_20
# http://hub.qgis.org/wiki/quantum-gis/Python_plugin_API_changes_from_18_to_20
def api_changes_for_version_20(fileToCheck):
    # check if file is cpp
#    if not re.match(".*cpp$", fileToCheck):
#        return    
    print "*** %s:%s - on file: " % (logtail, sys._getframe().f_code.co_name) + fileToCheck

    # list of sting to check
    checkList = [("QgsSearchString", "To be removed"),
                 ("QgsSearchTreeNode", "To be removed"),
                 ("QgsRasterBandStats", "Removed histogram related members (moved to QgsRasterHistogram)"),
                 ("bandStatistics", "Removed QgsRasterDataProvider method: replaced by QgsRasterBandStats bandStatistics( int theBandNo, const QgsRectangle & theExtent = QgsRectangle(), int theSampleSize = 0 )"),
                 ("populateHistogram", "Removed QgsRasterDataProvider method: void populateHistogram( int theBandNoInt, QgsRasterBandStats & theBandStats, int theBinCountInt = RASTER_HISTOGRAM_BINS, bool theIgnoreOutOfRangeFlag = true, bool theThoroughBandScanFlag = false ) \n replaced by virtual QgsRasterHistogram histogram( int theBandNo, int theBinCount = 0, double theMinimum = std::numeric_limits<double>::quiet_NaN(), double theMaximum = std::numeric_limits<double>::quiet_NaN(), const QgsRectangle & theExtent = QgsRectangle(), int theSampleSize = 0, bool theIncludeOutOfRange = false );"),
                 ("identify", "Removed QgsRasterDataProvider method: bool identify( const QgsPoint & point, QMap<QString, QString>& results )"),
                 ("identify", "Removed QgsRasterDataProvider method: QMap<int, void *> identify( const QgsPoint & point )"),
                 ("identifyAsText", "Removed QgsRasterDataProvider method: QString identifyAsText( const QgsPoint& point )"),
                 ("identifyAsHtml", "Removed QgsRasterDataProvider method: QString identifyAsHtml( const QgsPoint& point )"),
                 ("addLayers", "Removed QgsRasterDataProvider method: virtual void addLayers( const QStringList & layers, const QStringList & styles = QStringList() ) = 0;"),
                 ("supportedImageEncodings", "Removed QgsRasterDataProvider method: virtual QStringList supportedImageEncodings() = 0;"),
                 ("imageEncoding", "Removed QgsRasterDataProvider method: virtual QString imageEncoding() const = 0"),
                 ("setImageEncoding", "Removed QgsRasterDataProvider method: virtual void setImageEncoding( const QString & mimeType ) = 0"),
                 ("setImageCrs", "Removed QgsRasterDataProvider method: virtual void setImageCrs( const QString & crs ) = 0"),
                 ("listSvgFiles", "moved from QgsSvgMarkerSymbolLayerV2 to QgsSymbolLayerV2Utils"),
                 ("listSvgFilesAt", "moved from QgsSvgMarkerSymbolLayerV2 to QgsSymbolLayerV2Utils"),
                 ("symbolNameToPath", "moved from QgsSvgMarkerSymbolLayerV2 to QgsSymbolLayerV2Utils"),
                 ("symbolPathToName", "moved from QgsSvgMarkerSymbolLayerV2 to QgsSymbolLayerV2Utils"),
                 ("addRasterLayer", "Removed QgisApp method: addRasterLayer( QString const &rasterLayerPath, QString const &baseName, QString const &providerKey, QStringList const & layers, QStringList const & styles, QString const &format, QString const &crs )"),
                 ("rasterContrastEnhancement", "Removed QgisApp method: QgsContrastEnhancement* rasterContrastEnhancement( QgsRasterLayer* rlayer, int band, bool visibleAreaOnly = false ) const"),
                 ("histogramStretch", "Removed QgisApp method: void histogramStretch( bool visibleAreaOnly = false) \n Changed to void histogramStretch( bool visibleAreaOnly = false, QgsRasterLayer::ContrastEnhancementLimits theLimits = QgsRasterLayer::ContrastEnhancementMinMax )"),
                 ("addRasterLayer", "Removed QgisAppInterface method: addRasterLayer( const QString& url, const QString& baseName, const QString& providerKey, const QStringList& layers, const QStringList& styles, const QString& format, const QString& crs ) \n Replaced by addRasterLayer( const QString& url, const QString& baseName, const QString& providerKey)"),
                 ("QgsRasterLayer", "Removed QgsRasterLayer method: QgsRasterLayer( int dummy, const QString & baseName = QString(), const QString & path = QString(), const QString & providerLib = QString(), const QStringList & layers = QStringList(), const QStringList & styles = QStringList(), const QString & format = QString(), const QString & crs = QString() ); Replaced by QgsRasterLayer( const QString & uri, const QString & baseName, const QString & providerKey, bool loadDefaultStyleFlag = true );"),
                 ("setDataProvider", "Removed QgsRasterLayer method: setDataProvider( QString const & provider, QStringList const & layers, QStringList const & styles, QString const & format, QString const & theCrs, bool loadDefaultStyleFlag ) Replaced by setDataProvider( QString const & provider)"),
                 ("setDataProvider", "Removed QgsRasterLayer method: setDataProvider( QString const & provider, QStringList const & layers, QStringList const & styles, QString const & format, QString const & theCrs ) Replaced by setDataProvider( QString const & provider)"),
                 ("hasCachedHistogram", "Removed QgsRasterLayer method: bool hasCachedHistogram( int theBandNoInt, int theBinCountInt = RASTER_HISTOGRAM_BINS ) Use provider hasHistogram()"),
                 ("populateHistogram", "Removed QgsRasterLayer method: void populateHistogram( int theBandNoInt, int theBinCountInt = RASTER_HISTOGRAM_BINS, bool theIgnoreOutOfRangeFlag = true, bool theThoroughBandScanFlag = false ) Use provider histogram()"),
                 ("hasStatistics", "Removed QgsRasterLayer method: bool hasStatistics( int theBandNoInt ) Use provider hasStatistics()"),
                 ("QgsRasterBandStats", "Removed QgsRasterLayer method: const QgsRasterBandStats bandStatistics( int ) Use provider bandsStatistics()"),
                 ("QgsRasterBandStats", "Removed QgsRasterLayer method: const QgsRasterBandStats bandStatistics( const QString & ) Use provider bandsStatistics()"),
                 ("colorTable", "Removed QgsRasterLayer method: QList<QgsColorRampShader::ColorRampItem>* QgsRasterLayer::colorTable( int theBandNo ) Changed to QList<QgsColorRampShader::ColorRampItem> QgsRasterLayer::colorTable( int theBandNo )"),
                 ("grayBandName", "Removed QgsRasterLayer method: QString grayBandName() const Use QgsRasterRenderer and subclasses to get/set how the raster is displayed ( QgsRasterLayer::renderer() )"),
                 ("greenBandName", "Removed QgsRasterLayer method: QString greenBandName() const Use QgsRasterRenderer and subclasses to get/set how the raster is displayed ( QgsRasterLayer::renderer() )"),
                 ("invertHistogram", "Removed QgsRasterLayer method: bool invertHistogram() const Use QgsRasterRenderer and subclasses to get/set how the raster is displayed ( QgsRasterLayer::renderer() )"),
                 ("rasterTransparency", "Removed QgsRasterLayer method: QgsRasterTransparency* rasterTransparency() Use QgsRasterRenderer and subclasses to get/set how the raster is displayed ( QgsRasterLayer::renderer() )"),
                 ("rasterShader", "Removed QgsRasterLayer method: QgsRasterShader* rasterShader() Use QgsRasterRenderer and subclasses to get/set how the raster is displayed ( QgsRasterLayer::renderer() )"),
                 ("redBandName", "Removed QgsRasterLayer method: QString redBandName() const Use QgsRasterRenderer and subclasses to get/set how the raster is displayed ( QgsRasterLayer::renderer() )"),
                 ("transparentBandName", "Removed QgsRasterLayer method: QString transparentBandName() const Use QgsRasterRenderer and subclasses to get/set how the raster is displayed ( QgsRasterLayer::renderer() )"),
                 ("isGrayMinimumMaximumEstimated", "Removed QgsRasterLayer method: bool isGrayMinimumMaximumEstimated() const Functions related to statistics are now in QgsRasterDataProvider"),
                 ("setGrayMinimumMaximumEstimated", "Removed QgsRasterLayer method: void setGrayMinimumMaximumEstimated( bool theBool ) Functions related to statistics are now in QgsRasterDataProvider"),
                 ("isRGBMinimumMaximumEstimated", "Removed QgsRasterLayer method: bool isRGBMinimumMaximumEstimated() const Functions related to statistics are now in QgsRasterDataProvider"),
                 ("setRGBMinimumMaximumEstimated", "Removed QgsRasterLayer method: void setRGBMinimumMaximumEstimated( bool theBool ) Functions related to statistics are now in QgsRasterDataProvider"),
                 ("identify", "Removed QgsRasterLayer method: bool identify( const QgsPoint & point, QMap<QString, QString>& results )identify method available in QgsRasterDataProvider"),
                 ("identify", "Removed QgsRasterLayer method: bool identify( const QgsPoint & point, QMap<int, QString>& results ) identify method available in QgsRasterDataProvider"),
                 ("identifyAsText", "Removed QgsRasterLayer method: QString identifyAsText( const QgsPoint & point ) identify method available in QgsRasterDataProvider"),
                 ("identifyAsHtml", "Removed QgsRasterLayer method: QString identifyAsHtml( const QgsPoint & point ) identify method available in QgsRasterDataProvider"),
                 ("buildSupportedRasterFileFilter", "Removed QgsRasterLayer method: static void buildSupportedRasterFileFilter( QString & fileFilters ) Use QgsProviderRegistry::instance()->fileRasterFilters()"),
                 ("addComposerLabel", "Removed QgsComposerView method: addComposerLabel"),
                 ("addComposerMap", "Removed QgsComposerView method: addComposerMap"),
                 ("addComposerScaleBar", "Removed QgsComposerView method: addComposerScaleBar"),
                 ("addComposerLegend", "Removed QgsComposerView method: addComposerLegend"),
                 ("addComposerPicture", "Removed QgsComposerView method: addComposerPicture"),
                 ("addComposerShape", "Removed QgsComposerView method: addComposerShape"),
                 ("addComposerTable", "Removed QgsComposerView method: addComposerTable"),
                 ("pushAddRemoveCommand", "Removed QgsComposerView method: pushAddRemoveCommand"),
                 ("sendItemAddedSignal", "Removed QgsComposerView method: sendItemAddedSignal"),
                 ("composerLabelAdded", "Removed QgsComposerView signal: composerLabelAdded To port 1.x plugins, use the corresponding methods and signals of QgsComposition"),
                 ("composerMapAdded", "Removed QgsComposerView signal: composerMapAdded To port 1.x plugins, use the corresponding methods and signals of QgsComposition"),
                 ("composerScaleBarAdded", "Removed QgsComposerView signal: composerScaleBarAdded To port 1.x plugins, use the corresponding methods and signals of QgsComposition"),
                 ("composerLegendAdded", "Removed QgsComposerView signal: composerLegendAdded To port 1.x plugins, use the corresponding methods and signals of QgsComposition"),
                 ("composerPictureAdded", "Removed QgsComposerView signal: composerPictureAdded To port 1.x plugins, use the corresponding methods and signals of QgsComposition"),
                 ("setGridAnnotationPosition", "Removed QgsComposerMap  method: setGridAnnotationPosition( GridAnnotationPosition p ) Replaced by setGridAnnotationPosition( GridAnnotationPosition p, QgsComposerMap::Border border )"),
                 ("gridAnnotationPosition", "Removed QgsComposerMap  method: gridAnnotationPosition() Replaced by gridAnnotationPosition( QgsComposerMap::Border border ) "),
                 ("setGridAnnotationDirection", "Removed QgsComposerMap  method: setGridAnnotationDirection( GridAnnotationDirection d ) Replaced by setGridAnnotationDirection( GridAnnotationDirection d, QgsComposerMap::Border border )"),
                 ("gridAnnotationDirection", "Removed QgsComposerMap  method: gridAnnotationDirection() Replaced by gridAnnotationDirection( QgsComposerMap::Border border )"),
                 ("selectedEpsg()", "Deprecated QgsProjectionSelector method: selectedEpsg() Removed, there are other authorities - use selectedAuthId()"),
                 ("setSelectedEpsg", "Deprecated QgsProjectionSelector method: setSelectedEpsg( long epsg ) Removed, there are other authorities - so not always defined. Use setSelectedAuthId( QString authId )"),
                 ("pixmap()", "Deprecated QgsMapCanvasMap method: pixmap() Removed, use paintDevice() "),
                 ("canvasPixmap", "Deprecated QgsMapCanvas method: canvasPixmap Removed, use canvasPaintDevice()"),
                 ("selectedProj4String", "Deprecated QgsGenericProjectionSelector method: selectedProj4String"),
                 ("setSelectedEpsg", "Deprecated QgsGenericProjectionSelector method: setSelectedEpsg Removed, use other authorities: setSelectedCrsName( QString theName ), setSelectedCrsId( long theID ), setSelectedAuthId( QString authId )"),
                 ("selectedEpsg", "Deprecated QgsGenericProjectionSelector method: selectedEpsg There are other authorities - selectedCrsId() and selectedAuthId()"),
                ]
    check(checkList, fileToCheck)

def python_plugin_api_changes_from_18_to_20(fileToCheck):
#    if not re.match(".*py$", fileToCheck):
#        return
    print "*** %s:%s - on file: " % (logtail, sys._getframe().f_code.co_name) + fileToCheck

    # list of sting to check
    checkList = [("toBool()", "To be removed due belongs to QString"),
                 ("toString()", "To be removed"),
                 ("endsWith(", "QString method to substitute with endswith(...)"),
                 ("startsWith(", "QString method to substitute with startswith(...)"),
                 ("toList()", "To be removed"),
                 ("toInt()", "To be removed"),
                 ("toFloat()", "To be removed"),
                 ("toDouble()", "To be removed"),
                 ("toStringList()", "To be removed"),
                 ("toByteArray()", "To be removed"),
                 ("toPyObject()", "To be removed"),
                 ("QVariant(", "To be removed and used native type"),
                 ("QString(", "To be removed"),
                 ("QString.", "To be removed"),
                 ("QSettings", "Check The type of QSettings return values is specified in the QSettings.value() call. More info:"),
                 ("QStringList", "Raplace QStringList (and related method) with native python string "),
                 ("QList", "QList Use native list method"),
                 ("emit(SIGNAL", "Substitute SIGNAL emit with <signalname> = QtCore.pyqtSignal(<paramtype>) in self.<signalname>.emit(<paramtype parameters>)"),
                 ("QObject.connect(self.iface,SIGNAL", "Substitute QObject.connect(self.iface,SIGNAL('projectRead ()'),self.readSettings)  in self.iface.projectRead.connect(self.readSettings)"),
                 ("nextFeature(", "Substitude use of nextFeature(feture) iterating in layer.getFeatures([<QgsFeatureRequest>])"),
                 ("attributeMap", "Instead of use of attributeMap use directory fieldname as in fieldvalue=f[fieldname]"),
                 ("select(", "Instead use QgsVectorLayer.getFeatures(QgsFeatureRequest(...))"),
                 ("featureAtId(", "Instead use QgsVectorLayer.getFeatures(QgsFeatureRequest(...))"),
                ]
    check(checkList, fileToCheck)
    
def python_generic_things_to_check(fileToCheck):
#     if not re.match(".*py$", fileToCheck):
#         return
    print "*** %s:%s - on file: " % (logtail, sys._getframe().f_code.co_name) + fileToCheck

    # list of sting to check
    checkList = [("iteritems)", "To be removed substitude enumerating or generator")]
    check(checkList, fileToCheck)

def checkapi(fileToCheck):
    api_changes_for_version_20(fileToCheck)
    python_plugin_api_changes_from_18_to_20(fileToCheck)
    python_generic_things_to_check(fileToCheck)
    
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
        
    for opt, value in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
            
    if len(args) != 1:
        usage()
        sys.exit(2)
    
    # get path to parse and check if it's a dir o file
    pathtoparse = args[0]
    if not os.path.isdir(pathtoparse) and not os.path.isfile(pathtoparse):
        raise  ValueError("%s is not a path or file" % pathtoparse)
    
    # parse path or file
    if os.path.isfile(pathtoparse):
        filetoparse = pathtoparse
        checkapi(filetoparse)
    else:
        for (path, dirs, files) in os.walk(pathtoparse, True, walkerror, True):
            for file in files:
                filetoparse = os.path.join(path, file)
                checkapi(filetoparse)
        
    
if __name__ == "__main__":
    logtail = os.path.basename(sys.argv[0])
    main(sys.argv[1:])
