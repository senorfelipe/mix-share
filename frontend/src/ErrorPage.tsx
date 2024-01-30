import {
  Alert,
  AlertDescription,
  AlertIcon,
  AlertTitle,
} from '@chakra-ui/react';
import { useRouteError } from 'react-router-dom';

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <Alert
      status="error"
      variant="subtle"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      textAlign="center"
      height="200px"
    >
      <AlertIcon boxSize="40px" mr={0} />
      <AlertTitle mt={4} mb={1} fontSize="lg">
        Ooops!
      </AlertTitle>
      <AlertDescription maxWidth="sm">
        <p>Sorry, an unexpected error has occurred:</p>
        <code>{error.statusText || error.message}</code>
      </AlertDescription>
    </Alert>
  );
}
