#include<Servo.h>
String incomingCommand = "";

String targetColor;

Servo base;
Servo shoulder;
Servo elbow;
Servo gripper;


int gripperstart = 20;
int gripperend = 67;
int elbowstart = 90;
int shoulderstart=0 ;
int basestart =90;

int baseredball=87;
int shoulderredball=120;
int elbowredball=107;

int baseyellowball=87;
int shoulderyellowball=120;
int elbowyellowball=107;


int basegreenball=87;
int shouldergreenball=120;
int elbowgreenball=107;

int baseredbox=150;
int shoulderredbox=70;
int elbowredbox=90;

int baseyellowbox=130;
int shoulderyellowbox=70;
int elbowyellowbox=90;

int basegreenbox=25;
int shouldergreenbox=70;
int elbowgreenbox=90;









void setup() {
  // put your setup code here, to run once:
     Serial.begin(9600);
      pinMode(13, OUTPUT);
    base.attach(7);
    elbow.attach(3);
   gripper.attach(9);
   shoulder.attach(5);

  base.write(basestart);
  shoulder.write(shoulderstart);
  elbow.write(elbowstart);
  gripper.write(gripperstart);

  delay(2000);

   movetostart();
  
  

}

void loop() {
  // put your main code here, to run repeatedly:
 if (Serial.available() > 0) {
    incomingCommand = Serial.readStringUntil('\n');

     if (incomingCommand.startsWith("PICK ")) {
      
      int firstSpace = incomingCommand.indexOf(' ');
      int firstComma = incomingCommand.indexOf(',');
      targetColor = incomingCommand.substring(firstSpace + 1, firstComma);
      
     

    Serial.print("I read this line: ");
    Serial.println(incomingCommand);
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
   

    pickBall();
    delay(1000);
    gotobox();
    delay(1000);
    movetostart();
   Serial.println("DONE");
   delay(7000);

   }
}
}


void move(Servo servo, int start, int end){
  if( start > end){
    for(int i = start;i>=end;i--){
     servo.write(i);
     delay(70);
    }
  }
    else{
      for(int i = start;i<=end;i++){
     servo.write(i);
     delay(70);
    }
}
}





void pickBall(){

  if(targetColor == "red ball"){
    move(elbow, elbowstart , elbowredball);
     delay(500);
    //   move(base,basestart,baseredball);
    //  delay(2000);
      move(shoulder,shoulderstart,shoulderredball);
     delay(500);
     move(gripper, gripperstart , gripperend);
     delay(500);
     move(shoulder,shoulderredball,shoulderstart);
     delay(500);
  }
  else if(targetColor == "yellow ball"){
      move(elbow, elbowstart , elbowyellowball);
     delay(500);
    //   move(base,basestart,baseredball);
    //  delay(2000);
      move(shoulder,shoulderstart,shoulderyellowball);
     delay(500);
     move(gripper, gripperstart , gripperend);
     delay(500);
     move(shoulder,shoulderyellowball,shoulderstart);
     delay(500);
  }
  else if(targetColor == "green ball"){
      move(elbow, elbowstart , elbowgreenball);
     delay(500);
    //   move(base,basestart,baseredball);
    //  delay(2000);
      move(shoulder,shoulderstart,shouldergreenball);
     delay(500);
     move(gripper, gripperstart , gripperend);
     delay(500);
     move(shoulder,shouldergreenball,shoulderstart);
     delay(500);
  }
}




void gotobox(){

  if(targetColor == "red ball"){
     move(base, baseredball , baseredbox);
     delay(500);
     move(elbow,elbowredball,elbowredbox);
     delay(500);
     move(shoulder,shoulderstart,shoulderredbox);
     delay(500);
     move(gripper, gripperend , gripperstart);
     delay(500);
  }
  else if(targetColor == "yellow ball"){
    move(base, baseyellowball , baseyellowbox);
     delay(500);
     move(elbow,elbowyellowball,elbowyellowbox);
     delay(500);
     move(shoulder,shoulderstart,shoulderyellowbox);
     delay(500);
     move(gripper, gripperend , gripperstart);
     delay(500);
  }
  else if(targetColor == "green ball"){
   move(base, basegreenball , basegreenbox);
     delay(500);
     move(elbow,elbowgreenball,elbowgreenbox);
     delay(500);
     move(shoulder,shoulderstart,shouldergreenbox);
     delay(500);
     move(gripper, gripperend , gripperstart);
     delay(500);
  }
}



void movetostart() {
  move(base,base.read(), basestart);

   move(shoulder,shoulder.read(), shoulderstart);
   
 move(elbow,elbow.read(),elbowstart);

 move(gripper, gripper.read(), gripperstart);
}


