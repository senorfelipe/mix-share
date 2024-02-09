import { RouterProvider, createBrowserRouter } from "react-router-dom";
import ErrorPage from "../ErrorPage";
import HomePage from "../pages/HomePage";
import Login from "../pages/Login";
import { MixesPage } from "../pages/MixesPage";
import { UserProfile } from "../pages/UserProfile";
import { useAuth } from "../service/AuthProvider";
import { ProtectedRoute } from "./ProtectedRoute";

const Routes = () => {
  const { token } = useAuth();

  const routesForPublic = [
    {
      path: "/service",
      element: <div>Service Page</div>,
      errorElement: <ErrorPage />,
    },
    {
      path: "/about-us",
      element: <div>About Us</div>,
      errorElement: <ErrorPage />,
    },
  ];

  const routesForAuthenticatedOnly = [
    {
      path: "/",
      element: <ProtectedRoute />,
      errorElement: <ErrorPage />,
      children: [
        {
          path: "/",
          element: <MixesPage />,
        },
        {
          path: "/profile",
          element: <UserProfile />,
        },
      ],
    },
  ];

  const routesForNotAuthenticatedOnly = [
    {
      path: "/",
      element: <HomePage />,
    },
    {
      path: "/login",
      element: <Login />,
    },
  ];

  const router = createBrowserRouter([
    ...routesForPublic,
    ...(!token ? routesForNotAuthenticatedOnly : []),
    ...routesForAuthenticatedOnly,
  ]);

  return <RouterProvider router={router} />;
};

export default Routes;
