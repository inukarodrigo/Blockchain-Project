import React, { useState } from "react";
import { Navbar, Welcome, Footer, Services, Transactions } from "./components";

const App = () => {
  const [userEmail, setUserEmail] = useState("");

  const handleLogin = (email) => {
    setUserEmail(email);
  };

  return (
    <div className="min-h-screen">
      <div className="gradient-bg-welcome">
        <Navbar onLogin={handleLogin} />
        <Welcome userEmail={userEmail} />
      </div>
      <Services />
      <Transactions />
      <Footer />
    </div>
  );
};

export default App;
