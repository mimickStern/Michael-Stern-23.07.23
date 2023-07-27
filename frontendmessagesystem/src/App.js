import "./App.css";
import { useContext, useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Store } from "./Store";
import MessagesBoxScreen from "./screens/MessagesBoxScreen";
import SignupScreen from "./screens/SignUpScreen";
import SigninScreen from "./screens/SignInScreen";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";
import { LinkContainer } from "react-router-bootstrap";
import Nav from "react-bootstrap/Nav";
import ProtectedRoute from "./components/ProtectedRoute";
import { Tabs, Tab } from "react-bootstrap";
import HomeScreen from "./screens/HomeScreen";

function App() {
  const { state, dispatch: ctxDispatch } = useContext(Store);
  const { userInfo } = state;
  const [activeTab, setActiveTab] = useState("received");

  

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  const signoutHandler = () => {
    localStorage.removeItem("userInfo");
    ctxDispatch({ type: "USER_SIGNOUT" });
    window.location.href = "/signin";
  };


 

  return (
    <div className="App">
      <BrowserRouter>
        <ToastContainer position="top-center" limit={1} />
        <header>
          <Navbar bg="dark" variant="dark" expand="lg">
            <Container>
              <LinkContainer to="/signup">
                <Navbar.Brand> Message System</Navbar.Brand>
              </LinkContainer>
              {!userInfo ? (
                <Nav>
                  <Link className="nav-link" to="/signin">
                    Sign In
                  </Link>
                </Nav>
              ) : (
                <Nav>
                    <Link
                      className="nav-link"
                      to="#signout"
                      onClick={signoutHandler}
                    >
                      Sign Out
                    </Link>
                  </Nav>
              )}
            </Container>
          </Navbar>
        </header>
        <main>
          {userInfo && (
            <Tabs
              defaultActiveKey={activeTab}
              onSelect={(tab) => handleTabChange(tab)}
              animation={false}
              id="noanim-tab-example"
            >
              <Tab eventKey="received" title="Received Messages">
                {activeTab === "received" && (
                  <ProtectedRoute><MessagesBoxScreen messageType="received" /></ProtectedRoute>
                )}{" "}
              </Tab>
              <Tab eventKey="sent" title="Sent Messages">
                {activeTab === "sent" && (
                  <ProtectedRoute><MessagesBoxScreen messageType="sent" /></ProtectedRoute>
                )}
              </Tab>
              <Tab eventKey="read" title="Read Messages">
                {activeTab === "read" && (
                  <ProtectedRoute><MessagesBoxScreen messageType="read" /></ProtectedRoute>
                )}
              </Tab>
              <Tab eventKey="unread" title="Unread Messages">
                {activeTab === "unread" && (
                  <ProtectedRoute><MessagesBoxScreen messageType="unread" /></ProtectedRoute>
                )}
              </Tab>
              <Tab eventKey="create" title="Create Message">
                {activeTab === "create" && (
                  <ProtectedRoute><MessagesBoxScreen messageType="create" /></ProtectedRoute>
                )}
              </Tab>
            </Tabs>
          )}

          <Container>
            <Routes>
              <Route path="/signup" element={<SignupScreen />} />
              <Route path="/signin" element={<SigninScreen />} />
              <Route path="/" element={<HomeScreen/>}/>
            </Routes>
          </Container>
        </main>
        <footer>
          <div className="text-center">@2023 All rights reserved</div>
        </footer>
      </BrowserRouter>
    </div>
  );
}

export default App;
