import Featured from "../components/Featured";
import HighestGrossingActors from "../components/HighestGrossingActors";
import RecentReviews from "../components/RecentReviews";

const Home = () => {
  return (
    <div className="flex flex-col justify-start items-start w-2/3 mx-auto mb-10">
      <Featured />
      <RecentReviews />
      <HighestGrossingActors />
    </div>
  )
}

export default Home;