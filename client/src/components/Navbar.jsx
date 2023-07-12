import React, { useRef } from "react";
import { HiMenuAlt4 } from "react-icons/hi";
import { AiOutlineClose } from "react-icons/ai";
import emailjs from "@emailjs/browser";
import logo from "../../images/logo.png";

const NavBarItem = ({ title, classprops }) => (
  <li className={`mx-4 cursor-pointer ${classprops}`}>{title}</li>
);

const Navbar = () => {
  const [toggleMenu, setToggleMenu] = React.useState(false);
  const form = useRef();

  // 1. Output of the AI model needs to be passed to this function
  // 2. Based on the result of the model (1 or 0), the function has to decide if the email needs to be send or not
  const sendEmail = (e) => {
    e.preventDefault();

    emailjs.sendForm("service_9d4gy53", "template_r3t69sp", form.current, "wORxbtBe_xIcUzQi7")
      .then((result) => {
        console.log(result.text);
      }, (error) => {
        console.log(error.text);
      });
  };
  return (
    <nav className="w-full flex md:justify-center justify-between items-center p-4">
      <div className="md:flex-[0.5] flex-initial justify-center items-center">
        <img src={logo} alt="logo" className="w-32 cursor-pointer" />
      </div>
      <div className="right-j">
        <ul className="text-white md:flex hidden list-none flex-row justify-between items-center flex-initial">
          <form ref={form} className="email-container" onSubmit={sendEmail}>
            <input type="email" name="user_email" placeholder="Enter your Email address" />
            <button className="btn btn-j">Login</button>
          </form>
        </ul>
      </div>
      <div className="flex relative">
        {!toggleMenu && (
          <HiMenuAlt4 fontSize={28} className="text-white md:hidden cursor-pointer" onClick={() => setToggleMenu(true)} />
        )}
        {toggleMenu && (
          <AiOutlineClose fontSize={28} className="text-white md:hidden cursor-pointer" onClick={() => setToggleMenu(false)} />
        )}
        {toggleMenu && (
          <ul
            className="z-10 fixed -top-0 -right-2 p-3 w-[70vw] h-screen shadow-2xl md:hidden list-none
            flex flex-col justify-start items-end rounded-md blue-glassmorphism text-white animate-slide-in"
          >
            <li className="text-xl w-full my-2"><AiOutlineClose onClick={() => setToggleMenu(false)} /></li>
            {["Market", "Exchange", "Tutorials", "Wallets"].map(
              (item, index) => <NavBarItem key={item + index} title={item} classprops="my-2 text-lg" />,
            )}
          </ul>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
