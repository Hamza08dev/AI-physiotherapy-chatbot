import { render, screen } from "@testing-library/react";
import ChatPage from "../ChatPage";
import { MemoryRouter } from "react-router-dom";

// Mock Chatbot component
jest.mock("../../components/Chatbot", () => () => <div>Mock Chatbot</div>);

describe("ChatPage", () => {
  beforeEach(() => {
    // Clear any previous localStorage state
    localStorage.clear();
  });

  test("redirects to login if no token is present", () => {
    render(
      <MemoryRouter>
        <ChatPage />
      </MemoryRouter>
    );

    // Since it navigates using `useNavigate`, we'll just check that the fallback message appears
    expect(screen.getByText(/you must be logged in/i)).toBeInTheDocument();
  });

  test("shows Chatbot component when token is present", async () => {
    localStorage.setItem("token", "test-token");

    render(
      <MemoryRouter>
        <ChatPage />
      </MemoryRouter>
    );

    expect(await screen.findByText("Mock Chatbot")).toBeInTheDocument();
  });
});
