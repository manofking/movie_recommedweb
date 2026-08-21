import React, { useEffect, useState } from "react";
import "./Nav.css";

const Nav = () => {
  const [show, handleShow] = useState(false);

  useEffect(() => {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        handleShow(true);
      } else {
        handleShow(false);
      }
    });
    return () => {
      window.removeEventListener("scroll", () => {});
    };
  }, []);

  return (
    <nav className={`nav ${show && "nav__black"}`}>
      <img
        alt="DQflex logo"
        src="/dqflex_logo.png"
        className="nav__logo"
      />
      {/* public 폴더의 favicon_bu.ico */}
      <img
        alt="User logged"
        src="/favicon_bu.ico"
        className="nav__avatar"
      />
    </nav>
  );
};

export default Nav;
