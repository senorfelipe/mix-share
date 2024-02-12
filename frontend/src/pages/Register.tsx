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
import { Api } from "../axios/api";
import { PasswordInput } from "../components/PasswordInput";
import { useAuth } from "../service/AuthProvider";
import { AxiosHeaders } from "axios";

export const Register = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [registrationFailed, setRegistrationFailed] = useState(false);
  const [submitTried, setSubmitTried] = useState(false);
  const [errorMessages, setErrorMessages] = useState<string[]>([]);
  const navigate = useNavigate();
  const { setToken } = useAuth();

  const passwordsValid =
    password.length >= 8 &&
    passwordConfirm.length >= 8 &&
    password === passwordConfirm;

  const passwordFeedbackMsg =
    "Passwords must be the same and minimum 8 characters";

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

  const isValidInput = () => {
    return passwordsValid && isValidEmail() && !!username;
  };

  const handleRegistration = () => {
    if (!isValidInput()) {
      console.log("no valid input");
      setSubmitTried(true);
      return;
    }
    Api.renewInstance().post("/user/register", {
      email: email,
      username: username,
      password: password,
    })
      .then((response) => {
        if (response.status === 201) {
          setRegistrationFailed(false);
          setToken(response.data["access"]);
          navigate("/");
        }
      })
      .catch((error) => {
        setErrorMessages([]);
        setRegistrationFailed(true);
        if (error.response?.status !== 500 && error.response?.data) {
          for (const k in error.response.data) {
            setErrorMessages((msg) => [...msg, error.response.data[k]]);
          }
        } else {
          setErrorMessages([error.message]);
        }
      });
  };

  return (
    <Container mt={"3rem"}>
      <Box boxSize="lg">
        <Heading size="lg" mb="0.8rem">
          Create new Account
        </Heading>
        <VStack align="stretch">
          <FormControl isInvalid={submitTried && !isValidEmail()}>
            <FormLabel>Email</FormLabel>
            <Input
              id="useremail"
              type="email"
              placeholder="Enter Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="on"
            />
            {!isValidEmail() && (
              <FormErrorMessage>
                Please check your provided email
              </FormErrorMessage>
            )}
          </FormControl>
          <FormControl isInvalid={submitTried && !username}>
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
          <FormControl isInvalid={submitTried && !passwordsValid}>
            <FormLabel>Password</FormLabel>
            <PasswordInput
              inputId="userpasword"
              password={password}
              onChange={setPassword}
            />
            {!passwordsValid && (
              <FormErrorMessage>{passwordFeedbackMsg}</FormErrorMessage>
            )}
          </FormControl>
          <FormControl isInvalid={submitTried && !passwordsValid}>
            <FormLabel>Confirm Password</FormLabel>
            <PasswordInput
              inputId="userpaswordconfirm"
              password={passwordConfirm}
              onChange={setPasswordConfirm}
            />
            {!passwordsValid && (
              <FormErrorMessage>{passwordFeedbackMsg}</FormErrorMessage>
            )}
          </FormControl>
          <Button colorScheme="teal" onClick={() => handleRegistration()}>
            Create Account
          </Button>
          {registrationFailed && (
            <Alert status="error">
              <AlertIcon />
              <AlertTitle>Oooops</AlertTitle>
              <Spacer />
              <AlertDescription>
                {
                  <ul>
                    {errorMessages.map((msg) => (
                      <li>{msg}</li>
                    ))}
                  </ul>
                }
              </AlertDescription>
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
