<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.4-Hannover" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" maxScale="0" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal fetchMode="0" enabled="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour" enabled="false"/>
    </provider>
    <rasterrenderer band="1" type="paletted" nodataColor="" opacity="1" alphaBand="-1">
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
        <paletteEntry label="Canne à sucre" color="#fbfe2a" alpha="255" value="1"/>
        <paletteEntry label="Prairie pâturées" color="#44f414" alpha="255" value="2"/>
        <paletteEntry label="Prairie fauchées" color="#53ebb8" alpha="255" value="3"/>
        <paletteEntry label="Ananas" color="#fb7405" alpha="255" value="4"/>
        <paletteEntry label="Autres cultures maraichères" color="#d7d79e" alpha="255" value="5"/>
        <paletteEntry label="Sous serre ou ombrage" color="#cc0101" alpha="255" value="6"/>
        <paletteEntry label="Verger agrume" color="#7030a0" alpha="255" value="7"/>
        <paletteEntry label="Verger de letchi ou longani" color="#b889db" alpha="255" value="8"/>
        <paletteEntry label="Verger de manguier" color="#dcc5ed" alpha="255" value="9"/>
        <paletteEntry label="Plantation de cocotier" color="#dd4fc2" alpha="255" value="10"/>
        <paletteEntry label="Plantation de bananier" color="#891b74" alpha="255" value="11"/>
        <paletteEntry label="Forets et fourres de montagne" color="#364d1f" alpha="255" value="12"/>
        <paletteEntry label="Autre végétation arborée" color="#72ac3e" alpha="255" value="13"/>
        <paletteEntry label="Plantation forestière" color="#01a884" alpha="255" value="14"/>
        <paletteEntry label="Végétation altimontaine" color="#a9d08e" alpha="255" value="15"/>
        <paletteEntry label="Lande de rempart" color="#84bf4d" alpha="255" value="16"/>
        <paletteEntry label="Savane herbasée de basse altitude" color="#cac10c" alpha="255" value="17"/>
        <paletteEntry label="Végétation arbustive" color="#7c7607" alpha="255" value="18"/>
        <paletteEntry label="Massif de vigne maronne" color="#83d31a" alpha="255" value="19"/>
        <paletteEntry label="Végétation naturelle sur coulée de lave" color="#9adf5a" alpha="255" value="20"/>
        <paletteEntry label="Rochers et sol nu sans ou avec peu de végétation" color="#b67412" alpha="255" value="21"/>
        <paletteEntry label="Ombre due au relief" color="#606060" alpha="255" value="22"/>
        <paletteEntry label="Marais" color="#00768e" alpha="255" value="23"/>
        <paletteEntry label="Surface en eau" color="#01cccc" alpha="255" value="24"/>
        <paletteEntry label="Surface bâtie" color="#ff0101" alpha="255" value="25"/>
        <paletteEntry label="Panneau photovoltaïque" color="#ffabab" alpha="255" value="26"/>
        <paletteEntry label="Route et parking" color="#d2b2c5" alpha="255" value="27"/>
      </colorPalette>
      <colorramp type="randomcolors" name="[source]"/>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation colorizeStrength="100" saturation="0" grayscaleMode="0" colorizeOn="0" colorizeRed="255" colorizeBlue="128" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
