import {
  Alert,
  AlertDescription,
  AlertIcon,
  AlertTitle,
  Box,
  Button,
  Container,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Spacer,
  StackDivider,
  VStack,
} from "@chakra-ui/react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { PasswordInput } from "../components/PasswordInput";
import { API } from "../axios";

export const Register = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [registrationFailed, setRegistrationFailed] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const passwordsValid =
    !!password && !!passwordConfirm && password === passwordConfirm;

  const isValidEmail = () => {
    return (
      !!email &&
      String(email)
        .toLowerCase()
        .match(
          /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        )
    );
  };

  const handleRegistration = () => {
    if (!passwordsValid || !isValidEmail() || !username) {
      setErrorMessage("Please check your inputs once again :)");
      setRegistrationFailed(true);
      setSubmitted(true);
    } else {
      setRegistrationFailed(false);
      API.post("/user/register", {
        email: email,
        username: username,
        password: password,
      });
    }
  };

  return (
    <Container mt={"3rem"}>
      <Box boxSize="lg">
        <Heading size="lg" mb="0.8rem">
          SIGN UP
        </Heading>
        <VStack align="stretch">
          <FormControl isInvalid={submitted && !isValidEmail()}>
            <FormLabel>Email</FormLabel>
            <Input
              id="useremail"
              type="email"
              placeholder="Enter Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="on"
            />
          </FormControl>
          <FormControl isInvalid={submitted && !username}>
            <FormLabel>Username</FormLabel>
            <Input
              id="username"
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="on"
            />
          </FormControl>
          <FormControl isInvalid={submitted && !passwordsValid}>
            <FormLabel>Password</FormLabel>
            <PasswordInput
              inputId="userpasword"
              password={password}
              onChange={setPassword}
            />
            {!passwordsValid && (
              <FormErrorMessage>Passwords are not equal :S</FormErrorMessage>
            )}
          </FormControl>
          <FormControl isInvalid={submitted && !passwordsValid}>
            <FormLabel>Confirm Password</FormLabel>
            <PasswordInput
              inputId="userpaswordconfirm"
              password={passwordConfirm}
              onChange={setPasswordConfirm}
            />
            {!passwordsValid && (
              <FormErrorMessage>Passwords are not equal :S</FormErrorMessage>
            )}
          </FormControl>
          <Button colorScheme="teal" onClick={() => handleRegistration()}>
            Register
          </Button>
          {registrationFailed && (
            <Alert status="error">
              <AlertIcon />
              <AlertTitle>Registration failed :O</AlertTitle>
              <AlertDescription>{errorMessage}</AlertDescription>
            </Alert>
          )}
          <StackDivider height={"0.3rem"}></StackDivider>
          <Button
            colorScheme="real"
            variant="outline"
            onClick={() => navigate("/login")}
          >
            Alreday having an account?
          </Button>
        </VStack>
      </Box>
    </Container>
  );
};
