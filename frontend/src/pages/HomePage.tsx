import {
  Box,
  Button,
  ButtonGroup,
  Center,
  Container,
  Flex,
  Heading,
  Image,
  Spacer,
  Text,
} from '@chakra-ui/react';

import { useNavigate } from 'react-router-dom';

import classes from '../styles/root.module.css';
import image from '../assets/craiyon_181154_techno_dj_controller_setup_close_view.png';

export const HomePage = () => {
  const navigate = useNavigate();

  return (
    <>
      <Flex
        className={classes.rootMenu}
        p={3}
        minWidth="max-content"
        alignItems="center"
        gap="2"
      >
        <Box p="2">
          <Heading size="lg">Mixit</Heading>
        </Box>
        <Spacer />
        <ButtonGroup gap="2">
          <Button
            variant="outline"
            colorScheme="teal"
            onClick={() => navigate('/register')}
          >
            Sign up
          </Button>
          <Button colorScheme="teal" onClick={() => navigate('/login')}>
            Log in
          </Button>
        </ButtonGroup>
      </Flex>
      <Container>
        <Center mt={'2rem'}>
          <Text fontSize="2.5rem" as="b" pb="1rem" textAlign="center">
            Share your Mixes and learn togehter
          </Text>
        </Center>
        <Image src={image} />
      </Container>
    </>
  );
};

export default HomePage;
