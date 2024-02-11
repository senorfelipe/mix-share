import {
  Alert,
  AlertDescription,
  AlertIcon,
  AlertTitle,
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  StackDivider,
  VStack,
} from "@chakra-ui/react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../axios";
import { PasswordInput } from "../components/PasswordInput";
import { useAuth } from "../service/AuthProvider";

const Login = () => {
  const { setToken } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [loginFailed, setLoginFailed] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [password, setPassword] = useState("");

  const LOGIN_PATH = "/user/login";

  const handleLogin = () => {
    API.post(LOGIN_PATH, { email, password })
      .then((response) => {
        console.log("login data: " + response.data["access"]);
        setToken(response.data["access"]);
        navigate("/", { replace: true });
      })
      .catch((error) => {
        setLoginFailed(true);
        console.log(JSON.stringify(error));
        const message =
          error.response?.status === 401
            ? "Check your email and password."
            : error.message;
        setErrorMessage(message);
      });
  };

  return (
    <Container mt={"3rem"}>
      <Box>
        <Heading size="lg" mb="0.8rem" transform="capitalize">
          LOGIN
        </Heading>
        <VStack align="stretch">
          <FormControl>
            <FormLabel>Email</FormLabel>
            <Input
              id="useremail"
              type="email"
              placeholder="Enter Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <FormLabel>Password</FormLabel>
            <PasswordInput password={password} onChange={setPassword} />
          </FormControl>
          <Button colorScheme="teal" onClick={() => handleLogin()}>
            Login
          </Button>
          {loginFailed && (
            <Alert status="error">
              <AlertIcon />
              <AlertTitle>Login failed :O</AlertTitle>
              <AlertDescription>{errorMessage}</AlertDescription>
            </Alert>
          )}
          <StackDivider height={"0.3rem"}></StackDivider>
          <Button
            colorScheme="real"
            variant="outline"
            onClick={() => navigate("/register")}
          >
            Create New Account
          </Button>
        </VStack>
      </Box>
    </Container>
  );
};

export default Login;
