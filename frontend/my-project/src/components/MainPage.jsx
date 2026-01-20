import { Navbar } from "./Navbar";
import { HeroPage } from "./HeroPage";
import  FitnessTab  from "./FitnessTab"

export default function MainPage() {
  return (
    <div className="size-full">
      <Navbar />
      <FitnessTab/>
      {/* <HeroPage /> */}
    </div>
  );
}
