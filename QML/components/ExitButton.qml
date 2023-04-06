import QtQuick 2.15
import QtQuick.Controls.Material 2.15

Button {
    id: exitButton
    width: 30
    height: 30


    Image {

        id: backgroundImage
        anchors.top : parent.top
        anchors.left : parent.left
        anchors.right: parent.right
        anchors.bottom : parent.bottom

        source : exitButton.hovered ? "../images/redexit.svg" : "../images/greenexit.svg"
        sourceSize : Qt.size(30, 30)
    }

}
