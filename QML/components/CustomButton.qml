import QtQuick 2.15
import QtQuick.Controls.Material 2.15

Button {
    id : customBtn

    property color colorDefault : "#A2D729"
    property color colorMouseOver : "#E5446D"
    property color colorPressed : "#B73657"

    text: qsTr("LOGIN")

    QtObject {
        id : internal
        property var dynamicColor : if(customBtn.down){
                                        customBtn.down ? colorPressed : colorDefault
                                    } else {
                                        customBtn.hovered ? colorMouseOver : colorDefault
                                    }
    }


    background : Rectangle {
        implicitWidth : 260
        implicitHeight : 40
        opacity: enabled ? 1 : 0.3
        color : internal.dynamicColor
        radius : 10
    }

    contentItem: Text {
        id : textBtn
        text: customBtn.text
        color : "#F8F4E3"
        horizontalAlignment : Text.AlignHCenter
        verticalAlignment : Text.AlignVCenter
        font.bold: true
        font.family: "Inter"
        font.pointSize: 12
    }

}
