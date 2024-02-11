import {
  InputGroup,
  Input,
  InputRightElement,
  Button,
  Box,
  FormControl,
} from "@chakra-ui/react";
import React from "react";

interface PasswordInputProps {
  password: string;
  onChange: (password: string) => void;
  inputId?: string;
}

export function PasswordInput(props: PasswordInputProps) {
  const [show, setShow] = React.useState(false);
  const handleClick = () => setShow(!show);

  return (
    <InputGroup size="md">
      <Input
        id={props.inputId}
        pr="4.5rem"
        type={show ? "text" : "password"}
        placeholder="Enter password"
        value={props.password}
        onChange={(e) => props.onChange(e.target.value)}
      />
      <InputRightElement width="4.5rem">
        <Button h="1.75rem" size="sm" onClick={handleClick}>
          {show ? "Hide" : "Show"}
        </Button>
      </InputRightElement>
    </InputGroup>
  );
}
