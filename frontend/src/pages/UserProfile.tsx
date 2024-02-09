import { useEffect, useState } from "react";
import { API } from "../axios";

export const UserProfile = () => {
  const [profile, setProfile] = useState({
    fullName: "",
    avatar: "",
    bio: "",
    location: "",
  });

  useEffect(() => {
    API.get("/user/profiles/3").then((response) => {
      console.log("response data profiles: " + response.data);
      setProfile(response.data);
    });
  }, []);

  return (
    <div>
      <label>Full Name:</label>
      <label>{profile.fullName}</label>
      <label>location:</label>
      <label>{profile.location}</label>
      <label>About me:</label>
      <label>{profile.bio}</label>
    </div>
  );
};
