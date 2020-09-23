## Arcade

---

Arcade is a simple, portable scripting language for creating custom visualizations, labeling expressions, and much more.

For more infomation, visit the Arcade [Homepage](https://developers.arcgis.com/arcade/).

This folder will be organized by Arcade [Profile](https://developers.arcgis.com/arcade/guide/profiles/). A **profile** is a context in which an Arcade expression is evaluated and understood. They expect specific inputs and output types depending on the use case.

### Dashboard

`dashboard`

The [Dashboard profile](https://developers.arcgis.com/arcade/guide/profiles/#dashboard) is used for the list and indicator elements in the ArcGIS Dashboards Beta. An expression can be written to customize the way elements render data points. It is expected that the script returns a dictionary of name-value pairs specific for the element.

### Labeling

`labeling`

The [Labeling profile](https://developers.arcgis.com/arcade/guide/profiles/#labeling) allows the map author to write an expression that determines the label to show on the map for each feature. The script evaluates for each label as it is to be drawn. It is expected that the script returns a text value, comprising the label to be drawn.

### Popup

`popup`

With the [Popup profile](https://developers.arcgis.com/arcade/guide/profiles/#popup), map authors can write expressions that return values for display in the view's popup. Expressions can be referenced in the popup content's text template, field tables, and media charts. When the popup displays, the script will execute using the feature's attributes as variables in the expression. The script should return either text, a number, or date and place it in the table cell or text comprising the popup's content. Values returned for charts will be used as the basis for the data-driven chart.

### Visualization

`visualization`

The [Visualization profile](https://developers.arcgis.com/arcade/guide/profiles/#visualization) allows the map author to write an expression that evaluates to a value used to drive the visualization. This could be used for a visual variable such as size, or as a value in a class breaks renderer. When the feature is to be drawn, the script will be evaluated. It is expected that the script returns a value specific to the rendering property being calculated (e.g. A number for a class breaks visualization or text for a unique value visualization).
