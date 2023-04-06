import QtQuick 2.15
import QtQuick.Controls.Material 2.15

TextField {
    id: field
    implicitWidth : 260
    implicitHeight : 60

    placeholderText : qsTr("API Key")
    placeholderTextColor : "#F8F4E3"
    selectedTextColor : "#F8F4E3"

    Material.theme : Material.Dark
    Material.accent: "#A2D729"
    Material.foreground : "#A2D729"

}
