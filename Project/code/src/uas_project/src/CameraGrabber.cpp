#include "ros/ros.h"
#include "opencv2/opencv.hpp"
#include "std_msgs/String.h"
#include <cv_bridge/cv_bridge.h>

using namespace std;
using namespace cv;
/*

Mat cameraFrame;
VideoCapture camera(0); // Open default camera 0

if (!camera.isOpened())
{
    cout << "ERROR: Cannot open camera!" << endl;
    return;
}

while (1)
{
    camera.read(cameraFrame);   // Grab image from webcam

    imshow("Webcam", cameraFrame);

    if( waitKey(25) == 27 ) // Frame rate: 25ms, stop capturing by pressing ESC.
        break;
}*/

int main(int argc, char **argv)
{
    /*
    Mat cameraFrame;
    VideoCapture camera(0); // Open default camera 0

    if (!camera.isOpened())
    {
        cout << "ERROR: Cannot open camera!" << endl;
        return 0;
    }

    while (1)
    {
        camera.read(cameraFrame);   // Grab image from webcam

        imshow("Webcam", cameraFrame);

        if( waitKey(25) == 27 ) // Frame rate: 25ms, stop capturing by pressing ESC.
            break;
    }*/


    ros::init(argc, argv, "image_grabber");
    ros::NodeHandle nh;
    ros::Publisher pub = nh.advertise<std_msgs::String>("camera_image", 1000);

    Mat cameraFrame;
    VideoCapture camera(0); // Open default camera 0

    if (!camera.isOpened())
    {
        cout << "ERROR: Cannot open camera!" << endl;
        return 0;
    }

    while(1)
    {
        camera.read(cameraFrame);   // Grab image from webcam

        //sensor_msgs::ImagePtr toImageMsg() const;
        //void toImageMsg(sensor_msgs::Image& ros_image) const;
        sensor_msgs::ImagePtr img = toImageMsg(cameraFrame);

        std_msgs::String msg;
        pub.publish(msg);
        ros::spinOnce();
    }

    return 0;
}
