import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { my_api_key } from ".env";
export const geminiApi = createApi({
  reducerPath: "geminiApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "https://generativelanguage.googleapis.com/v1beta/",
  }),
  endpoints: (builder) => ({
    sendChatPrompt: builder.mutation({
      query: ({ prompt, systemContext, isJson }) => ({
        url: `models/gemini-2.5-flash-preview-09-2025:generateContent?key=${my_api_key}`,
        method: "POST",
        body: {
          contents: [
            {
              parts: [
                {
                  text: systemContext
                    ? `${systemContext}\n\nUser Query: ${prompt}`
                    : prompt,
                },
              ],
            },
          ],
          generationConfig: isJson
            ? { responseMimeType: "application/json" }
            : {},
        },
      }),
      transformResponse: (response) =>
        response.candidates?.[0]?.content?.parts?.[0]?.text,
    }),
  }),
});

export const { useSendChatPromptMutation } = geminiApi;
