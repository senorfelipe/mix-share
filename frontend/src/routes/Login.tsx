import {
  Button,
  Container,
  FormControl,
  FormLabel,
  Input,
  StackDivider,
  VStack,
} from "@chakra-ui/react";
import { useState } from "react";
import { PasswordInput } from "../components/PasswordInput";
import axios from "axios";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const LOGIN_URL = "http://127.0.0.1:8000/api/user/login";

  const handleLogin = () => {
    axios.post(LOGIN_URL, { email, password }).then((response) => {
      alert("You sent log in request")
      console.log(response.data);
    });
  };

  return (
    <Container mt={"3rem"}>
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
        <StackDivider height={"0.3rem"}></StackDivider>
        <Button colorScheme="real" variant="outline">
          Create New Account
        </Button>
      </VStack>
    </Container>
  );
};

export default Login;
