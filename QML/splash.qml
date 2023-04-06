import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls.Material 2.15
import "components"
import "fonts"
import "images"

Window
{
    id: splash
    visible: true
    width: 400; height: 500

    flags: Qt.FramelessWindowHint | Qt.WA_TranslucentBackground
    color: "transparent"

    // Modified from Will Chen's Handler https://stackoverflow.com/questions/18927534/qtquick2-dragging-frameless-window
    Item {
        id: _dragHandler
        anchors.fill: parent
        DragHandler {
            acceptedDevices: PointerDevice.Mouse
            grabPermissions:  PointerHandler.CanTakeOverFromItems | PointerHandler.ApprovesTakeOverByAnything
            onActiveChanged: if (active) splash.startSystemMove()
        }
    }

    Rectangle {
        id: rectangle
        radius: 10
        anchors.fill : parent
        anchors.margins : 10
        color: "#292f36"

        MouseArea {
            id : mouseArea
            visible: true
            anchors.fill : parent
            onClicked : forceActiveFocus()

        }

        Image {
            id: logo
            x: 140
            y: 60
            width: 100
            height: 100
            source: "images/logo.png"
            fillMode: Image.PreserveAspectFit
        }

        Image {
            id: logotext
            x: 90
            y: 188
            source: "images/logotext.svg"
            fillMode: Image.PreserveAspectFit
        }

        CustomButton {
            id: customButton
            x: 60
            y: 383
        }

        CustomField {
            id: customField
            x: 70
            y: 306
            width: 240
        }

    }


}
