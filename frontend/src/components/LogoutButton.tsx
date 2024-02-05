import { useNavigate } from 'react-router-dom';
import { useAuth } from '../provider/AuthProvider';
import { Button } from '@chakra-ui/react';

const LogoutButton = () => {
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    setToken(null);
    navigate('/', { replace: true });
  };

  return (
    <Button colorScheme="red" variant="outline" onClick={() => handleLogout()}>
      Logout
    </Button>
  );
};

export default LogoutButton;
