import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/planning")({ component: () => <PageStub title="Planning" description="Weekoverzicht van alle evenementen, inpakwerk en bezorgingen. Gebruik nu Boekingen en Inpakken voor de bestaande functionaliteit." /> });
