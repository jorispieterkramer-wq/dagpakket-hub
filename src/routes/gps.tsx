import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/gps")({ component: () => <PageStub title="GPS tracking" description="Live voertuig-locaties op een Leaflet kaart, te activeren vanaf de iPad in het voertuig." /> });
