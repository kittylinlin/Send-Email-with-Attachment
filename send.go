package main

import (
	"fmt"
	"log"
	"bytes"
	"io/ioutil"

	"gopkg.in/gomail.v2"
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ses"
)

const (
    Sender = ""
    Recipient = ""
    Subject = "Send Attachment by AWS SES"
	Region = "us-west-2"
)

func main() {

	message := gomail.NewMessage()
	message.SetHeader("From", Sender)
	message.SetHeader("To", Recipient)
	message.SetHeader("Subject", Subject)

	textByte, err := ioutil.ReadFile("email.txt")
    if err != nil {
        log.Fatal(err)
    }
	message.SetBody("text/plain", string(textByte))

	htmlByte, err := ioutil.ReadFile("email.html")
    if err != nil {
        log.Fatal(err)
    }
	message.AddAlternative("text/html", string(htmlByte))

	// attach file
	message.Attach("corgi.pdf")

	buffer := new(bytes.Buffer)
	_, err = message.WriteTo(buffer)
	if err != nil {
		log.Fatal(err)
	}

	input := &ses.SendRawEmailInput{
		RawMessage:   &ses.RawMessage{
			Data: buffer.Bytes(),
		},
	}

    awsSession, err := session.NewSession(&aws.Config{
        Region: aws.String(Region)},
	)
	if err != nil {
		log.Fatal(err)
	}
    
    client := ses.New(awsSession)

    // Attempt to send the email.
    result, err := client.SendRawEmail(input)
    if err != nil {
		log.Fatal(err)
    }
    
    fmt.Println("Email Sent to address: " + Recipient)
    fmt.Println(result)
}
