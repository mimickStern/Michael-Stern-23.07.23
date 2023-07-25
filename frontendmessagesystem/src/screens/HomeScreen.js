import React, { useContext } from "react";
import { Store } from "../Store";
import { Container, Card } from "react-bootstrap";

const HomeScreen = () => {
  const { state } = useContext(Store);
  const { userInfo } = state;

  return (
    <div className="home-screen">
        {!userInfo && (
        <>
      <Container className="mt-5">
        <Card>
          <Card.Body>
            <Card.Title className="mb-4">
              Welcome to the Message System
            </Card.Title>
            <Card.Text className="mb-3">
              This is a simple message system application. You can use the
              navigation bar above to sign in or sign up, and then explore the
              messages under different tabs.
            </Card.Text>
            <Card.Text className="mb-3">
              The application allows you to send, receive, mark messages as read
              or unread, and more.
            </Card.Text>
          </Card.Body>
        </Card>
      </Container>
      </>
      )}
    </div>
  );
};

export default HomeScreen;
