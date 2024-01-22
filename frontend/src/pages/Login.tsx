import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  StackDivider,
  VStack,
} from "@chakra-ui/react";
import { PasswordInput } from "../components/PasswordInput";

export function Login() {
  return (
    <VStack align="stretch">
      <FormControl>
        <FormLabel>Email address</FormLabel>
        <Input type="email" placeholder="Enter Email" />
        <FormLabel>Password</FormLabel>
        <PasswordInput />
      </FormControl>
      <Button colorScheme="teal">Login</Button>
      <StackDivider height={"0.3rem"}></StackDivider>
      <Button colorScheme="real" variant="outline">
        Register
      </Button>
    </VStack>
  );
}
