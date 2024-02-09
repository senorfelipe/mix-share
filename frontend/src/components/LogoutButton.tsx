import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../service/AuthProvider";

const LogoutButton = () => {
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    setToken(null);
    navigate("/", { replace: true });
  };

  return (
    <Button colorScheme="red" variant="outline" onClick={() => handleLogout()}>
      Logout
    </Button>
  );
};

export default LogoutButton;
