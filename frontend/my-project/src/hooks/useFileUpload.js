import { useDispatch } from "react-redux";
import { setFileContext } from "../store/appSlice";
import { addMessage } from "../store/chatSlice";

export const useFileUpload = () => {
  const dispatch = useDispatch();

  const uploadFile = async (file) => {
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      dispatch(setFileContext({ name: file.name, content: e.target.result }));
      dispatch(
        addMessage({
          id: Date.now(),
          text: `Uploaded ${file.name}`,
          sender: "bot",
        })
      );
    };
    reader.readAsText(file);
  };

  return { uploadFile };
};
