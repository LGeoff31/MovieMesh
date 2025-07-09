import Featured from "../components/Featured";
import HighestGrossingActors from "../components/HighestGrossingActors";

const Home = () => {
  return (
    <>
      <Featured />
      {/* <h1 className="text-2xl font-bold">Recent Reviews</h1> */}
      <HighestGrossingActors />
    </>
  )
}

export default Home;