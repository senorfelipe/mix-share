import {
    Box,
    Card,
    CardBody,
    CardHeader,
    Container,
    Flex,
    Heading,
    Stack,
    StackDivider,
    Text,
    UnorderedList,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useApi } from "../axios";
import LogoutButton from "../components/LogoutButton";
import { IMix } from "../types";

export const MixesPage = () => {
  const [mixes, setMixes] = useState<IMix[]>([]);
  const { data, loading, error } = useApi({ url: "/mixes", method: "GET" });

  useEffect(() => {
    if (data) {
      setMixes(
        data.map((mix) => {
          return {
            user_id: mix.owner,
            name: mix.name,
            description: mix.description,
            uploadTime: mix.upload_time,
            fileLink: mix.file,
            lengthInSec: mix.length_in_sec,
          } as IMix;
        })
      );
    } else {
      setMixes([]);
    }
  }, [data]);

  if (loading) {
    return <></>;
  }

  return (
    <>
      <Container>
        <Flex justify="space-between" align="flex-start">
          <Heading>Mix List</Heading>
          <LogoutButton></LogoutButton>
        </Flex>
        <UnorderedList>
          {mixes.map((mix) => (
            <Card>
              <CardHeader>
                <Heading size="md">{mix.name}</Heading>
              </CardHeader>
              <CardBody>
                <Stack divider={<StackDivider />} spacing="4">
                  <Box>
                    <Heading size="xs" textTransform="uppercase">
                      description
                    </Heading>
                    <Text>{mix.description}</Text>
                  </Box>
                  <Box>
                    <Heading size="xs" textTransform="uppercase">
                      Uploaded
                    </Heading>
                    <Text>{new Date(mix.uploadTime).toLocaleString()}</Text>
                  </Box>
                </Stack>
              </CardBody>
            </Card>
          ))}
        </UnorderedList>
      </Container>
    </>
  );
};
