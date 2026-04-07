import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { store } from "./app/store";
import { BrowserRouter } from "react-router-dom";
import App from "./App";

import "./index.css";
import { loadFromStorage } from "./store/authSlice";
import AuthInitializer from "./components/AuthInitializer";

const savedAuth = localStorage.getItem("auth");

if (savedAuth) {
  try {
    store.dispatch(loadFromStorage(JSON.parse(savedAuth)));
  } catch (err) {
    console.error(err);
    localStorage.removeItem("auth");
  }
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <Provider store={store}>
    <BrowserRouter>
      <AuthInitializer>
        <App />
      </AuthInitializer>
    </BrowserRouter>
  </Provider>
);
