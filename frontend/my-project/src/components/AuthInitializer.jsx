import { useLoadUserQuery } from "../services/authApi";
import { useDispatch, useSelector } from "react-redux";
import { setCredentials, logout } from "../store/authSlice";
import { useEffect } from "react";

export default function AuthInitializer({ children }) {
  const dispatch = useDispatch();
  const authState = useSelector((state) => state.auth);

  const auth = JSON.parse(localStorage.getItem("auth") || "{}");

  const { data, error, isLoading } = useLoadUserQuery(undefined, {
    skip: !auth?.access, // 🔥 only run if token exists
  });

  useEffect(() => {
    if (data) {
      dispatch(
        setCredentials({
          user: data,
          access: authState.accessToken,
          refresh: authState.refreshToken,
        }),
      );
    }

    if (error) {
      dispatch(logout());
    }
  }, [data, error, dispatch]);

  if (isLoading) return <div>Loading...</div>;

  return children;
}
