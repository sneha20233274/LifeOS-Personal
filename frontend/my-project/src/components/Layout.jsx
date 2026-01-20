import { Outlet, useLocation } from "react-router-dom";
import { Navbar } from "./Navbar";

export default function Layout() {
  const location = useLocation();

  // ❌ Pages where navbar should NOT appear
  const hideNavbarRoutes = ["/show-plan"];

  const hideNavbar = hideNavbarRoutes.includes(location.pathname);

  return (
    <>
      {!hideNavbar && <Navbar />}
      <Outlet />
    </>
  );
}
