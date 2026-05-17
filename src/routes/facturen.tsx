import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/facturen")({ component: () => <PageStub title="Facturen & offertes" description="PDF factuur generator met BTW logica, Moneybird API koppeling en AI offerte generator." /> });
