  int LED = 13; // Pin digital para el LED
  char entrada; // Variable para guardar el valor del carácter enviado
   
  void setup()
  {
    pinMode(LED, OUTPUT); // Pin digital del LED como salida.
    Serial.begin(9600); // Velocidad de comunicación en baudios.
  }
   
  void loop()
  {
    int sensorValue = analogRead(A0);
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    float voltage = sensorValue * (5.0 / 1023.0);
    // print out the value you read:
    Serial.println(voltage);
    if (Serial.available() > 0) // Si se recibe un carácter...
    {
      entrada = Serial.read(); // Guardamos el valor del carácter en la variable entrada.
   
      if ((entrada=='D')||(entrada=='d')) // Si el carácter recibido es "D" o "d"
      {      
        digitalWrite(LED, HIGH); // Se enciende el LED


      }
      else if ((entrada=='I')||(entrada=='i')) // Si el carácter recibido es "I" o "i"    
      {
        digitalWrite(LED, LOW); // Se apaga el LED

      }
    }
    delay(500);
  }
