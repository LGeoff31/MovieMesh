import HighestGrossingActors from "../components/HighestGrossingActors";
import ActorsSearch from "../components/ActorsSearch";

const Actors = () => {
  return (
    <div className="flex flex-col w-2/3 mx-auto my-12">
      <ActorsSearch />
      <HighestGrossingActors />
    </div>
  );
};

export default Actors;