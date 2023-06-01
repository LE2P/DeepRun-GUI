<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.22.4-Białowieża" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" fetchMode="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="QString" name="WMSBackgroundLayer" value="false"/>
      <Option type="QString" name="WMSPublishDataSourceUrl" value="false"/>
      <Option type="QString" name="embeddedWidgets/count" value="0"/>
      <Option type="QString" name="identify/format" value="Value"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" name="name" value=""/>
      <Option name="properties"/>
      <Option type="QString" name="type" value="collection"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling zoomedInResamplingMethod="nearestNeighbour" maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour" enabled="false"/>
    </provider>
    <rasterrenderer type="paletted" nodataColor="" opacity="1" alphaBand="-1" band="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry value="1" label="Sugar Cane" alpha="255" color="#fbfe2a"/>
        <paletteEntry value="2" label="Grazed meadow" alpha="255" color="#44f414"/>
        <paletteEntry value="3" label="Mowed meadow" alpha="255" color="#53ebb8"/>
        <paletteEntry value="4" label="Pineapple" alpha="255" color="#fb7405"/>
        <paletteEntry value="5" label="Other vegetables" alpha="255" color="#d7d79e"/>
        <paletteEntry value="6" label="Greenhouse" alpha="255" color="#cc0101"/>
        <paletteEntry value="7" label="Citrus" alpha="255" color="#7030a0"/>
        <paletteEntry value="8" label="Lychee or longan" alpha="255" color="#b889db"/>
        <paletteEntry value="9" label="Mango" alpha="255" color="#dcc5ed"/>
        <paletteEntry value="10" label="Coconut" alpha="255" color="#dd4fc2"/>
        <paletteEntry value="11" label="Banana" alpha="255" color="#891b74"/>
        <paletteEntry value="12" label="Forest and mountains" alpha="255" color="#364d1f"/>
        <paletteEntry value="13" label="Other woody" alpha="255" color="#72ac3e"/>
        <paletteEntry value="14" label="Forest plantation" alpha="255" color="#01a884"/>
        <paletteEntry value="15" label="Altimontane vegetation" alpha="255" color="#a9d08e"/>
        <paletteEntry value="16" label="Rampart heath" alpha="255" color="#84bf4d"/>
        <paletteEntry value="17" label="Savanna" alpha="255" color="#cac10c"/>
        <paletteEntry value="18" label="Shrubby vegetation" alpha="255" color="#7c7607"/>
        <paletteEntry value="19" label="Giant bramble" alpha="255" color="#83d31a"/>
        <paletteEntry value="20" label="Vegetation on lava" alpha="255" color="#9adf5a"/>
        <paletteEntry value="21" label="Rock" alpha="255" color="#b67412"/>
        <paletteEntry value="22" label="Terrain shadow" alpha="255" color="#606060"/>
        <paletteEntry value="23" label="Swamp" alpha="255" color="#00768e"/>
        <paletteEntry value="24" label="Water area" alpha="255" color="#01cccc"/>
        <paletteEntry value="25" label="Building" alpha="255" color="#ff0101"/>
        <paletteEntry value="26" label="Photovoltaic farm" alpha="255" color="#ffabab"/>
        <paletteEntry value="27" label="Road and parking" alpha="255" color="#d2b2c5"/>
        <paletteEntry value="98" label="Clouds and shadows" alpha="255" color="#840b43"/>
      </colorPalette>
      <colorramp type="randomcolors" name="[source]">
        <Option/>
      </colorramp>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation grayscaleMode="0" colorizeRed="255" colorizeGreen="128" saturation="0" colorizeBlue="128" colorizeStrength="100" invertColors="0" colorizeOn="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
